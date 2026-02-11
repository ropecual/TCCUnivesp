from src.processamento_lote import processar_pasta_gpx
from src.enriquecimento_geografico import enriquecer_localizacao
from src.clustering_dificuldade import classificar_dificuldade_kmeans


def main():
    """
    Pipeline principal do projeto de classificação de dificuldade de trilhas.

    Etapas:
    1) Processamento dos arquivos GPX
    2) (Opcional) Enriquecimento geográfico
    3) Classificação da dificuldade via K-Means
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

    classificar_dificuldade_kmeans(
        caminho_csv_entrada=caminho_para_classificacao,
        caminho_csv_saida=caminho_classificado,
        n_clusters=5
    )

    print("\nPipeline completo executado com sucesso.")


if __name__ == "__main__":
    main()
