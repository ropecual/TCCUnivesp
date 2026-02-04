import gpxpy
import pandas as pd


def ler_gpx(caminho_gpx: str) -> pd.DataFrame:
    """
    Lê um arquivo GPX e retorna um DataFrame contendo:
    latitude, longitude, altitude (m) e tempo.
    """
    with open(caminho_gpx, 'r') as arquivo:
        gpx = gpxpy.parse(arquivo)

    pontos = []

    for trilha in gpx.tracks:
        for segmento in trilha.segments:
            for ponto in segmento.points:
                pontos.append({
                    'latitude': ponto.latitude,
                    'longitude': ponto.longitude,
                    'altitude_m': ponto.elevation,
                    'tempo': ponto.time
                })

    return pd.DataFrame(pontos)


def calcular_tempo_total_minutos(dados: pd.DataFrame) -> float:
    """
    Calcula o tempo total da trilha (em minutos) a partir
    do primeiro e do último timestamp do GPX.
    """
    inicio = dados['tempo'].iloc[0]
    fim = dados['tempo'].iloc[-1]

    return (fim - inicio).total_seconds() / 60
