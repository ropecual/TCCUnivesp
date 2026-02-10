from src.processamento_lote import processar_pasta_gpx
from scripts.enriquecer_localizacao import executar_enriquecimento
from scripts.classificar_dificuldade import executar_classificacao


def main():
    print("\n[1/3] Processando arquivos GPX...")

    pasta_gpx = 'dados/gpx'
    caminho_saida_analise = 'dados/resultados/analise_trilhas.csv'

    df_resultados = processar_pasta_gpx(pasta_gpx)

    df_resultados.to_csv(
        caminho_saida_analise,
        index=False,
        encoding='utf-8'
    )

    print(f"Arquivo salvo em: {caminho_saida_analise}")

    print("\n[2/3] Enriquecendo dados geográficos...")
    executar_enriquecimento()

    print("\n[3/3] Classificando dificuldade das trilhas...")
    executar_classificacao()

    print("\nPipeline completo executado com sucesso.")


if __name__ == "__main__":
    main()
