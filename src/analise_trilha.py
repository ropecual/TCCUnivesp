import os
import numpy as np
import pandas as pd

from src.leitura_gpx import (
    ler_gpx,
    calcular_tempo_total_minutos
)
from src.metricas_trilha import (
    calcular_distancia_total_km,
    calcular_ganho_elevacao_m,
    calcular_tempo_ativo_min
)
from src.modelos_tempo import (
    estimar_tempo_naismith_min,
    estimar_tempo_tobler_min
)

"""
As coordenadas geográficas iniciais de cada trilha foram extraídas diretamente
dos arquivos GPX e armazenadas como variáveis espaciais.

A identificação administrativa (cidade, estado e país) é realizada em etapa
posterior, de forma desacoplada do processamento principal, garantindo
reprodutibilidade metodológica.
"""

# ----------------------------------------------------------------------
# Funções auxiliares
# ----------------------------------------------------------------------

def calcular_inclinacao_media_graus(distancia_km: float, ganho_elevacao_m: float) -> float:
    if distancia_km <= 0:
        return 0.0

    inclinacao_rad = np.arctan(ganho_elevacao_m / (distancia_km * 1000))
    return float(np.degrees(inclinacao_rad))


def calcular_duracao_e_dias(dados: pd.DataFrame):
    if 'time' not in dados.columns:
        return None, 0, 'desconhecido'

    tempos = dados['time'].dropna()

    if len(tempos) < 2:
        return None, 0, 'desconhecido'

    inicio = tempos.iloc[0]
    fim = tempos.iloc[-1]

    duracao_total_h = (fim - inicio).total_seconds() / 3600
    dias_trilha = tempos.dt.date.nunique()

    tipo_trilha = 'single_day' if dias_trilha == 1 else 'multi_day'

    return float(duracao_total_h), int(dias_trilha), tipo_trilha


def gpx_tem_execucao_real(distancia_km: float, tempo_ativo_min: float) -> bool:
    """
    Verifica se o GPX representa uma execução real com base
    em critérios fisiológicos plausíveis.
    """
    if tempo_ativo_min is None or tempo_ativo_min <= 0 or distancia_km <= 0:
        return False

    velocidade_kmh = distancia_km / (tempo_ativo_min / 60)

    # Intervalo fisiologicamente plausível para trekking
    return 0.8 <= velocidade_kmh <= 6.5


# ----------------------------------------------------------------------
# Função principal
# ----------------------------------------------------------------------

def analisar_trilha(caminho_gpx: str) -> dict:

    nome_trilha = os.path.splitext(os.path.basename(caminho_gpx))[0]

    # ------------------------------------------------------------------
    # Leitura do GPX
    # ------------------------------------------------------------------
    dados = ler_gpx(caminho_gpx)

    latitude_inicio = float(dados.iloc[0]['latitude'])
    longitude_inicio = float(dados.iloc[0]['longitude'])

    # ------------------------------------------------------------------
    # Métricas geométricas globais
    # ------------------------------------------------------------------
    distancia_km = calcular_distancia_total_km(dados)
    ganho_elevacao_m = calcular_ganho_elevacao_m(dados)

    inclinacao_media = calcular_inclinacao_media_graus(
        distancia_km, ganho_elevacao_m
    )

    # ------------------------------------------------------------------
    # Estrutura temporal
    # ------------------------------------------------------------------
    duracao_total_h, dias_trilha, tipo_trilha = calcular_duracao_e_dias(dados)
    dias_validos = max(dias_trilha, 1)

    distancia_por_dia_km = distancia_km / dias_validos
    ganho_por_dia_m = ganho_elevacao_m / dias_validos

    inclinacao_media_dia = calcular_inclinacao_media_graus(
        distancia_por_dia_km, ganho_por_dia_m
    )

    # ------------------------------------------------------------------
    # Modelos clássicos (escala diária)
    # ------------------------------------------------------------------
    tempo_naismith_dia_min = estimar_tempo_naismith_min(
        distancia_por_dia_km, ganho_por_dia_m
    )

    tempo_tobler_dia_min = estimar_tempo_tobler_min(
        distancia_por_dia_km, inclinacao_media_dia
    )

    tempo_naismith_total_min = tempo_naismith_dia_min * dias_validos
    tempo_tobler_total_min = tempo_tobler_dia_min * dias_validos

    # ------------------------------------------------------------------
    # Tempos observados
    # ------------------------------------------------------------------
    tempo_decorrido_min = calcular_tempo_total_minutos(dados)
    tempo_ativo_real_min = calcular_tempo_ativo_min(dados)

    # ------------------------------------------------------------------
    # Seleção do tempo de referência (CORRIGIDA)
    # ------------------------------------------------------------------
    if gpx_tem_execucao_real(distancia_km, tempo_ativo_real_min):
        tempo_usado_min = tempo_ativo_real_min
        origem_tempo = 'ativo_real'

        erro_naismith_min = tempo_ativo_real_min - tempo_naismith_total_min
        erro_tobler_min = tempo_ativo_real_min - tempo_tobler_total_min
    else:
        tempo_usado_min = tempo_tobler_total_min
        origem_tempo = 'estimado_tobler'

        erro_naismith_min = None
        erro_tobler_min = None

    # ------------------------------------------------------------------
    # Retorno
    # ------------------------------------------------------------------
    return {
        'trilha': nome_trilha,
        'latitude_inicio': round(latitude_inicio, 6),
        'longitude_inicio': round(longitude_inicio, 6),

        'distancia_km': round(distancia_km, 3),
        'ganho_elevacao_m': round(ganho_elevacao_m, 1),
        'inclinacao_media_graus': round(inclinacao_media, 2),

        'duracao_total_h': round(duracao_total_h, 2) if duracao_total_h else None,
        'dias_trilha': dias_trilha,
        'tipo_trilha': tipo_trilha,

        'distancia_por_dia_km': round(distancia_por_dia_km, 2),
        'ganho_por_dia_m': round(ganho_por_dia_m, 1),

        'tempo_decorrido_min': round(tempo_decorrido_min, 2)
            if tempo_decorrido_min else None,

        'tempo_ativo_real_min': round(tempo_ativo_real_min, 2)
            if tempo_ativo_real_min else None,

        'tempo_naismith_min': round(tempo_naismith_total_min, 2),
        'tempo_tobler_min': round(tempo_tobler_total_min, 2),

        'tempo_usado_min': round(tempo_usado_min, 2),
        'origem_tempo': origem_tempo,

        'erro_naismith_min': round(erro_naismith_min, 2)
            if erro_naismith_min is not None else None,

        'erro_tobler_min': round(erro_tobler_min, 2)
            if erro_tobler_min is not None else None
    }
