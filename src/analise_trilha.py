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
foi realizada em etapa posterior, de forma desacoplada do processamento principal, 
a fim de garantir a reprodutibilidade do método
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


def analisar_trilha(caminho_gpx: str) -> dict:
	"""
	Executa a análise completa de uma trilha GPX e retorna
	um dicionário com métricas geométricas, topográficas e temporais.

	Este módulo não depende de serviços externos, garantindo
	reprodutibilidade e robustez do processamento.
	"""
	# Nome da trilha a partir do nome do arquivo
	nome_trilha = os.path.splitext(os.path.basename(caminho_gpx))[0]

	# Leitura do GPX
	dados = ler_gpx(caminho_gpx)

	# Coordenadas iniciais da trilha (para uso posterior em análises espaciais)
	latitude_inicio = float(dados.iloc[0]['latitude'])
	longitude_inicio = float(dados.iloc[0]['longitude'])

	# Métricas básicas
	distancia_km = calcular_distancia_total_km(dados)
	ganho_elevacao_m = calcular_ganho_elevacao_m(dados)
	tempo_real_min = calcular_tempo_total_minutos(dados)

	# Inclinação média
	inclinacao_media_graus = calcular_inclinacao_media_graus(
		distancia_km, ganho_elevacao_m
	)

	# Modelos de estimativa de tempo
	tempo_naismith_min = estimar_tempo_naismith_min(
		distancia_km, ganho_elevacao_m
	)

	tempo_tobler_min = estimar_tempo_tobler_min(
		distancia_km, inclinacao_media_graus
	)

	# Erros dos modelos
	erro_naismith_min = tempo_real_min - tempo_naismith_min
	erro_tobler_min = tempo_real_min - tempo_tobler_min

	return {
		'trilha': nome_trilha,
		'latitude_inicio': round(latitude_inicio, 6),
		'longitude_inicio': round(longitude_inicio, 6),
		'distancia_km': round(distancia_km, 3),
		'ganho_elevacao_m': round(ganho_elevacao_m, 1),
		'inclinacao_media_graus': round(inclinacao_media_graus, 2),
		'tempo_real_min': round(tempo_real_min, 2),
		'tempo_naismith_min': round(tempo_naismith_min, 2),
		'tempo_tobler_min': round(tempo_tobler_min, 2),
		'erro_naismith_min': round(erro_naismith_min, 2),
		'erro_tobler_min': round(erro_tobler_min, 2)
	}
