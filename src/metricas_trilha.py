from geopy.distance import geodesic
import pandas as pd




def calcular_tempo_ativo_min(
    dados: pd.DataFrame,
    vmin_kmh: float = 0.5,
    vmax_kmh: float = 7.0
) -> float:
    """
    Calcula o tempo ativo de deslocamento (em minutos),
    somando apenas os intervalos em que a velocidade instantânea
    é fisiologicamente plausível para caminhada.

    Esse método:
    - ignora paradas longas (acampamento, descanso, espera)
    - funciona para trilhas single-day e multi-day
    - funciona com GPX bruto ou simplificado
    """
    if 'time' not in dados.columns:
        return None

    tempo_ativo_min = 0.0

    for i in range(1, len(dados)):
        p0 = dados.iloc[i - 1]
        p1 = dados.iloc[i]

        if pd.isna(p0['time']) or pd.isna(p1['time']):
            continue

        delta_t_h = (p1['time'] - p0['time']).total_seconds() / 3600
        if delta_t_h <= 0:
            continue

        distancia_km = geodesic(
            (p0['latitude'], p0['longitude']),
            (p1['latitude'], p1['longitude'])
        ).km

        velocidade_kmh = distancia_km / delta_t_h if delta_t_h > 0 else 0

        if vmin_kmh <= velocidade_kmh <= vmax_kmh:
            tempo_ativo_min += delta_t_h * 60

    return round(tempo_ativo_min, 2)

def calcular_distancia_total_km(
    dados: pd.DataFrame,
    distancia_min_m: float = 1.0
) -> float:
    """
    Calcula a distância total da trilha em quilômetros,
    somando as distâncias geodésicas entre pontos consecutivos.

    distancia_min_m: ignora deslocamentos muito pequenos (ruído GPS)
    """
    distancia_total_m = 0.0

    for i in range(1, len(dados)):
        ponto_anterior = (
            dados.loc[i - 1, 'latitude'],
            dados.loc[i - 1, 'longitude']
        )
        ponto_atual = (
            dados.loc[i, 'latitude'],
            dados.loc[i, 'longitude']
        )

        d = geodesic(ponto_anterior, ponto_atual).meters

        if d >= distancia_min_m:
            distancia_total_m += d

    return distancia_total_m / 1000


def calcular_ganho_elevacao_m(
    dados: pd.DataFrame,
    delta_min_m: float = 3.0
) -> float:
    """
    Calcula o ganho de elevação positivo (em metros),
    ignorando pequenas oscilações verticais (ruído de sensor).

    delta_min_m: variação mínima de altitude para ser considerada subida real
    """
    ganho = 0.0
    altitudes = dados['altitude_m'].values

    for i in range(1, len(altitudes)):
        delta = altitudes[i] - altitudes[i - 1]

        if delta >= delta_min_m:
            ganho += delta

    return float(ganho)

