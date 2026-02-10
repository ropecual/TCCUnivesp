import gpxpy
import pandas as pd


def ler_gpx(caminho_gpx: str) -> pd.DataFrame:
    """
    Lê um arquivo GPX (bruto ou simplificado) e retorna um DataFrame
    contendo latitude, longitude, altitude (m) e timestamp.

    O método:
    - lê todos os pontos disponíveis (todos os tracks e segmentos)
    - remove pontos inválidos ou incompletos
    - normaliza timestamps para UTC
    - ordena cronologicamente
    """
    with open(caminho_gpx, 'r', encoding='utf-8') as arquivo:
        gpx = gpxpy.parse(arquivo)

    pontos = []

    for trilha in gpx.tracks:
        for segmento in trilha.segments:
            for ponto in segmento.points:
                if (
                    ponto.latitude is None or
                    ponto.longitude is None or
                    ponto.elevation is None
                ):
                    continue

                pontos.append({
                    'latitude': ponto.latitude,
                    'longitude': ponto.longitude,
                    'altitude_m': ponto.elevation,
                    'time': ponto.time
                })

    df = pd.DataFrame(pontos)

    if df.empty:
        raise ValueError(f"GPX sem pontos válidos: {caminho_gpx}")

    # ------------------------------------------------------------------
    # Normalização temporal
    # ------------------------------------------------------------------
    df['time'] = pd.to_datetime(df['time'], utc=True, errors='coerce')
    df = df.sort_values('time').reset_index(drop=True)

    return df


def calcular_tempo_total_minutos(dados: pd.DataFrame) -> float:
    """
    Calcula o tempo total da trilha em minutos com base
    no primeiro e último timestamp válido.

    Retorna None se o GPX não possuir timestamps suficientes.
    """
    if 'time' not in dados.columns:
        return None

    tempos_validos = dados['time'].dropna()

    if len(tempos_validos) < 2:
        return None

    inicio = tempos_validos.iloc[0]
    fim = tempos_validos.iloc[-1]

    return (fim - inicio).total_seconds() / 60
