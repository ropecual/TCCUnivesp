from src.enriquecimento_geografico import enriquecer_localizacao

def executar_enriquecimento():
    """
    Executa a etapa de geocodificação reversa com controle de taxa,
    cache local e tolerância a falhas.
    """
    enriquecer_localizacao(
        caminho_csv_entrada='dados/resultados/analise_trilhas.csv',
        caminho_csv_saida='dados/resultados/analise_trilhas_enriquecido.csv'
    )

    print("Enriquecimento geográfico concluído.")


if __name__ == "__main__":
    executar_enriquecimento()
