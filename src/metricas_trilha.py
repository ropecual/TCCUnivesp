from geopy.distance import geodesic
import pandas as pd




def calcular_tempo_ativo_min(
    dados: pd.DataFrame,
    vmin_kmh: float = 0.5,
    vmax_kmh: float = 7.0
) -> float:
    """
    Objetivo: Calcular o tempo de movimento efetivo dentro de padrões biomecânicos.
    Entrada: 
        - dados: pd.DataFrame com colunas ['latitude', 'longitude', 'time'].
        - vmin_kmh: Velocidade mínima (humanamente plausível para trilha).
        - vmax_kmh: Velocidade máxima (limite de corrida/movimento rápido).
    Processamento: 
        1. Itera entre pontos consecutivos calculando a distância geodésica.
        2. Calcula a velocidade instantânea entre os pontos.
        3. Acumula o delta temporal apenas se a velocidade estiver no intervalo [vmin, vmax].
    Saída: Float representando o tempo ativo acumulado em minutos.
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
    Objetivo: Determinar a quilometragem total percorrida no plano horizontal.
    Entrada: 
        - dados: pd.DataFrame com ['latitude', 'longitude'].
        - distancia_min_m: Filtro de ruído (ignora micro-movimentos do sinal GPS).
    Processamento: 
        1. Utiliza a biblioteca geopy para calcular a distância geodésica entre pontos 'i' e 'i-1'.
        2. Soma as distâncias que superam o limiar de ruído configurado.
    Saída: Float representando a distância total em quilômetros.
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
    Objetivo: Calcular o ganho acumulado de elevação positiva (desnível positivo).
    Entrada: 
        - dados: pd.DataFrame com a coluna 'altitude_m'.
        - delta_min_m: Limiar de variação para filtrar ruídos de sensores barométricos.
    Processamento: 
        1. Analisa a série temporal de altitudes.
        2. Soma apenas as variações positivas (subidas) que excedem o limiar de 3m.
    Saída: Float representando o ganho total em metros.
    """
    ganho = 0.0
    altitudes = dados['altitude_m'].values

    for i in range(1, len(altitudes)):
        delta = altitudes[i] - altitudes[i - 1]

        if delta >= delta_min_m:
            ganho += delta

    return float(ganho)

