from geopy.distance import geodesic
import pandas as pd


def calcular_distancia_total_km(dados: pd.DataFrame) -> float:
    """
    Calcula a distância total da trilha em quilômetros,
    somando as distâncias geodésicas entre pontos consecutivos.
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

        distancia_total_m += geodesic(ponto_anterior, ponto_atual).meters

    return distancia_total_m / 1000


def calcular_ganho_elevacao_m(dados: pd.DataFrame) -> float:
    """
    Calcula o ganho de elevação positivo (em metros),
    somando apenas as variações positivas de altitude.
    """
    variacao_altitude = dados['altitude_m'].diff()
    ganho_elevacao = variacao_altitude[variacao_altitude > 0].sum()

    return float(ganho_elevacao)
