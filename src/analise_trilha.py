import os
import numpy as np
import pandas as pd

from src.leitura_gpx import ler_gpx
from src.metricas_trilha import (
    calcular_distancia_total_km,
    calcular_ganho_elevacao_m
)
from src.modelos_tempo import estimar_tempo_tobler_min


# ------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------------------------------------

def calcular_inclinacao_media_graus(distancia_km: float, ganho_elevacao_m: float) -> float:
    """
    Objetivo: Calcular a inclinação média da trilha em termos angulares.
    Entrada: Distância horizontal (km) e Ganho de elevação (m).
    Processamento: 
        1. Converte distância para metros.
        2. Calcula a arco-tangente do gradiente (subida / vã).
        3. Converte o resultado de radianos para graus.
    Saída: Float representando a inclinação média em graus.
    """
    if distancia_km <= 0:
        return 0.0

    inclinacao_rad = np.arctan(
        ganho_elevacao_m / (distancia_km * 1000)
    )
    return float(np.degrees(inclinacao_rad))


def calcular_dias_trilha(dados: pd.DataFrame) -> int:
    """
    Objetivo: Diferenciar trilhas de um dia (leisure) de expedições multi-day.
    Entrada: pd.DataFrame com a coluna 'time'.
    Processamento: Extrai a parte da 'data' do timestamp e conta ocorrências únicas.
    Saída: Inteiro representando o número de dias de duração.
    """
    if 'time' not in dados.columns:
        return 1

    tempos = dados['time'].dropna()

    if len(tempos) < 2:
        return 1

    return int(tempos.dt.date.nunique())


def calcular_indice_concentracao(dados: pd.DataFrame) -> float:
    """
    Objetivo: Medir a heterogeneidade do esforço vertical ao longo dos dias.
    Entrada: pd.DataFrame com colunas 'time' e 'altitude_m'.
    Processamento: 
        1. Agrupa os pontos por data.
        2. Calcula o ganho de elevação de cada dia individualmente.
        3. Computa o Coeficiente de Variação (Desvio Padrão / Média) dos ganhos diários.
    Saída: Float representando a regularidade do esforço (0 = esforço constante).
    """
    if 'time' not in dados.columns:
        return 0.0

    df = dados.dropna(subset=['time']).copy()
    df['data'] = df['time'].dt.date

    ganhos = []

    for _, grupo in df.groupby('data'):
        ganho_dia = calcular_ganho_elevacao_m(grupo)
        ganhos.append(ganho_dia)

    if len(ganhos) <= 1:
        return 0.0

    media = np.mean(ganhos)
    if media == 0:
        return 0.0

    return float(np.std(ganhos) / media)
    return float(np.std(ganhos) / media)


# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def analisar_trilha(caminho_gpx: str) -> dict:
    """
    Objetivo: Orquestrar a extração completa de metadados científicos de uma trilha.
    Entrada: String com o caminho do arquivo GPX.
    Processamento: 
        1. Executa 'ler_gpx' para obter o DataFrame.
        2. Aciona o motor de métricas (distância, ganho, inclinação).
        3. Aplica o modelo de Tobler para estimativa de intensidade temporal.
        4. Calcula o score de Intensidade Diária (combinação de tempo e declividade).
    Saída: Dicionário contendo todos os indicadores calculados prontos para o dataset.
    """

    nome_trilha = os.path.splitext(
        os.path.basename(caminho_gpx)
    )[0]

    dados = ler_gpx(caminho_gpx)

    latitude_inicio = float(dados.iloc[0]['latitude'])
    longitude_inicio = float(dados.iloc[0]['longitude'])

    distancia_km = calcular_distancia_total_km(dados)
    ganho_elevacao_m = calcular_ganho_elevacao_m(dados)

    inclinacao_media = calcular_inclinacao_media_graus(
        distancia_km,
        ganho_elevacao_m
    )

    dias_trilha = max(calcular_dias_trilha(dados), 1)

    tipo_trilha = (
        'single_day' if dias_trilha == 1 else 'multi_day'
    )

    distancia_por_dia = distancia_km / dias_trilha

    ganho_por_km = (
        ganho_elevacao_m / distancia_km
        if distancia_km > 0 else 0
    )

    # ------------------------------------------------------------
    # TEMPO ESTIMADO VIA TOBLER
    # ------------------------------------------------------------

    tempo_estimado_dia_min = estimar_tempo_tobler_min(
        distancia_por_dia,
        inclinacao_media
    )

    tempo_por_km_dia = (
        tempo_estimado_dia_min / distancia_por_dia
        if distancia_por_dia > 0 else 0
    )

    # ------------------------------------------------------------
    # INTENSIDADE DIÁRIA (ESCALA ORIGINAL COERENTE)
    # ------------------------------------------------------------

    intensidade_diaria = (
        tempo_por_km_dia
        + ganho_por_km / 100
        + inclinacao_media
    )

    indice_concentracao = calcular_indice_concentracao(dados)

    return {
        'trilha': nome_trilha,
        'latitude_inicio': round(latitude_inicio, 6),
        'longitude_inicio': round(longitude_inicio, 6),
        'distancia_km': round(distancia_km, 3),
        'ganho_elevacao_m': round(ganho_elevacao_m, 1),
        'inclinacao_media_graus': round(inclinacao_media, 2),
        'dias_trilha': dias_trilha,
        'tipo_trilha': tipo_trilha,
        'intensidade_diaria': round(intensidade_diaria, 3),
        'indice_concentracao_esforco': round(indice_concentracao, 3)
    }
