import os
import numpy as np

from src.leitura_gpx import ler_gpx, calcular_tempo_total_minutos
from src.metricas_trilha import (
    calcular_distancia_total_km,
    calcular_ganho_elevacao_m
)
from src.modelos_tempo import (
    estimar_tempo_naismith_min,
    estimar_tempo_tobler_min
)

"""
As coordenadas geográficas iniciais de cada trilha foram extraídas diretamente dos arquivos GPX e
armazenadas como variáveis espaciais. A identificação administrativa (cidade, estado e país)
é realizada em etapa posterior, de forma desacoplada do processamento principal,
a fim de garantir a reprodutibilidade do método.
"""


def calcular_inclinacao_media_graus(distancia_km: float, ganho_elevacao_m: float) -> float:
    """
    Calcula a inclinação média da trilha em graus,
    a partir do ganho de elevação e da distância horizontal.
    """
    if distancia_km <= 0:
        return 0.0

    inclinacao_rad = np.arctan(ganho_elevacao_m / (distancia_km * 1000))
    return np.degrees(inclinacao_rad)


def gpx_tem_tempo_real(tempo_min: float, distancia_km: float) -> bool:
    """
    Verifica se o tempo presente no GPX é fisiologicamente plausível,
    indicando uma trilha efetivamente executada.
    """
    if tempo_min <= 0 or distancia_km <= 0:
        return False

    velocidade_kmh = distancia_km / (tempo_min / 60)

    # Intervalo fisiologicamente plausível para trekking
    return 1.0 <= velocidade_kmh <= 7.0


def analisar_trilha(caminho_gpx: str) -> dict:
    """
    Executa a análise completa de uma trilha GPX e retorna
    um dicionário com métricas geométricas, topográficas e temporais.

    O método admite dois modos:
    - GPX executado: utiliza tempo real observado
    - GPX planejado: utiliza tempo estimado por Tobler
    """
    # Nome da trilha a partir do nome do arquivo
    nome_trilha = os.path.splitext(os.path.basename(caminho_gpx))[0]

    # Leitura do GPX
    dados = ler_gpx(caminho_gpx)

    # Coordenadas iniciais
    latitude_inicio = float(dados.iloc[0]['latitude'])
    longitude_inicio = float(dados.iloc[0]['longitude'])

    # Métricas geométricas e topográficas
    distancia_km = calcular_distancia_total_km(dados)
    ganho_elevacao_m = calcular_ganho_elevacao_m(dados)
    inclinacao_media = calcular_inclinacao_media_graus(
        distancia_km, ganho_elevacao_m
    )

    # Modelos clássicos de tempo
    tempo_naismith_min = estimar_tempo_naismith_min(
        distancia_km, ganho_elevacao_m
    )
    tempo_tobler_min = estimar_tempo_tobler_min(
        distancia_km, inclinacao_media
    )

    # Tentativa de uso do tempo real
    tempo_real_min = calcular_tempo_total_minutos(dados)

    if gpx_tem_tempo_real(tempo_real_min, distancia_km):
        tempo_usado_min = tempo_real_min
        origem_tempo = 'real'
        erro_naismith_min = tempo_real_min - tempo_naismith_min
        erro_tobler_min = tempo_real_min - tempo_tobler_min
    else:
        # GPX planejado: usa Tobler como proxy de esforço
        tempo_usado_min = tempo_tobler_min
        origem_tempo = 'estimado_tobler'
        erro_naismith_min = None
        erro_tobler_min = None

    return {
        'trilha': nome_trilha,
        'latitude_inicio': round(latitude_inicio, 6),
        'longitude_inicio': round(longitude_inicio, 6),
        'distancia_km': round(distancia_km, 3),
        'ganho_elevacao_m': round(ganho_elevacao_m, 1),
        'inclinacao_media_graus': round(inclinacao_media, 2),

        'tempo_usado_min': round(tempo_usado_min, 2),
        'origem_tempo': origem_tempo,

        'tempo_real_min': round(tempo_real_min, 2) if origem_tempo == 'real' else None,
        'tempo_naismith_min': round(tempo_naismith_min, 2),
        'tempo_tobler_min': round(tempo_tobler_min, 2),

        'erro_naismith_min': round(erro_naismith_min, 2) if erro_naismith_min is not None else None,
        'erro_tobler_min': round(erro_tobler_min, 2) if erro_tobler_min is not None else None
    }
