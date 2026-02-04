from src.enriquecimento_geografico import enriquecer_localizacao
"""
A etapa de geocodificação reversa foi executada com controle rigoroso de taxa de requisições, 
incluindo atrasos explícitos, cache local e tolerância a falhas, 
em conformidade com as diretrizes de uso do serviço Nominatim.

"""
enriquecer_localizacao(
    caminho_csv_entrada='../dados/resultados/analise_trilhas.csv',
    caminho_csv_saida='../dados/resultados/analise_trilhas_enriquecido.csv'
)
