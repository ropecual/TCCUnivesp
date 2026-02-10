from src.clustering_dificuldade import classificar_dificuldade_kmeans


def executar_classificacao():
	"""
	A classificação da dificuldade das trilhas foi realizada por meio de um algoritmo de agrupamento não supervisionado (K-Means),
	utilizando variáveis derivadas de esforço relativo. As trilhas foram agrupadas em três clusters,
	posteriormente interpretados e rotulados como Leve, Moderada e Pesada, de acordo com os valores médios de tempo
	por quilômetro, ganho altimétrico por quilômetro e inclinação média.
	"""

	classificar_dificuldade_kmeans(
		caminho_csv_entrada='dados/resultados/analise_trilhas_enriquecido.csv',
		caminho_csv_saida='dados/resultados/trilhas_classificadas.csv',
		n_clusters=3
	)


if __name__ == "__main__":
	executar_classificacao()
