from src.processamento_lote import processar_pasta_gpx
from src.enriquecimento_geografico import enriquecer_localizacao
from src.clustering_dificuldade import classificar_dificuldade_kmeans, classificar_dificuldade_dbscan, classificar_dificuldade_hierarquico


def main():
    """
    Objetivo: Pipeline mestre do TCC Univesp.
    Fluxo:
    1. Ingestão e Processamento Lote: Transforma GPX em métricas tabulares iniciais.
    2. Enriquecimento (Opcional): Adiciona dados geocodificados através da API Nominatim.
    3. Modelagem e Classificação: Aplica Machine Learning para rotular as trilhas.
    """

    # ------------------------------------------------------------
    # CONFIGURAÇÕES
    # ------------------------------------------------------------

    pasta_gpx = 'dados/gpx'

    caminho_analise = 'dados/resultados/analise_trilhas.csv'
    caminho_enriquecido = 'dados/resultados/analise_trilhas_enriquecido.csv'
    caminho_classificado = 'dados/resultados/trilhas_classificadas.csv'

    calcular_localizacao = input(
        "\nDeseja executar o enriquecimento geográfico? (s/n): "
    ).strip().lower() == 's'

    # ------------------------------------------------------------
    # 1) Processamento GPX
    # ------------------------------------------------------------

    print("\n[1/3] Processando arquivos GPX...")

    df_resultados = processar_pasta_gpx(pasta_gpx)

    df_resultados.to_csv(
        caminho_analise,
        index=False,
        encoding='utf-8'
    )

    print(f"Arquivo salvo em: {caminho_analise}")

    # ------------------------------------------------------------
    # 2) Enriquecimento (Opcional)
    # ------------------------------------------------------------

    if calcular_localizacao:
        print("\n[2/3] Enriquecendo dados geográficos...")
        enriquecer_localizacao(
            caminho_csv_entrada=caminho_analise,
            caminho_csv_saida=caminho_enriquecido
        )
        print("Enriquecimento geográfico concluído.")
        caminho_para_classificacao = caminho_enriquecido
    else:
        print("\n[2/3] Enriquecimento ignorado.")
        caminho_para_classificacao = caminho_analise

    # ------------------------------------------------------------
    # 3) Classificação
    # ------------------------------------------------------------

    print("\n[3/3] Classificando dificuldade das trilhas...")

    # 3) Classificação Comparativa
    print("\n[3/3] Iniciando Comparação de Algoritmos de Clustering...")

    # K-Means (Base)
    print("\nExecutando K-Means...")
    classificar_dificuldade_kmeans(
        caminho_csv_entrada=caminho_para_classificacao,
        caminho_csv_saida='dados/resultados/trilhas_kmeans.csv',
        n_clusters=5
    )

    # Hierárquico
    print("\nExecutando Clustering Hierárquico...")
    classificar_dificuldade_hierarquico(
        caminho_csv_entrada=caminho_para_classificacao,
        caminho_csv_saida='dados/resultados/trilhas_hierarquico.csv',
        n_clusters=5
    )

    # DBSCAN
    print("\nExecutando DBSCAN...")
    classificar_dificuldade_dbscan(
        caminho_csv_entrada=caminho_para_classificacao,
        caminho_csv_saida='dados/resultados/trilhas_dbscan.csv',
        eps=0.5, 
        min_samples=3
    )

    print("\nAnálise comparativa completa. Verifique a pasta 'dados/resultados/'.")


if __name__ == "__main__":
    main()
