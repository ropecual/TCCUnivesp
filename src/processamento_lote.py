import os
import pandas as pd

from src.analise_trilha import analisar_trilha


def processar_pasta_gpx(caminho_pasta_gpx: str) -> pd.DataFrame:
    """
    Objetivo: Orquestrar o processamento massivo de arquivos geográficos (.gpx).
    Entrada: String com o caminho do diretório contendo os arquivos GPX.
    Processamento: 
        1. Varre o diretório em busca de arquivos com extensão .gpx.
        2. Para cada arquivo, invoca a função 'analisar_trilha'.
        3. Consolida os dicionários de resultados em uma lista.
        4. Transforma a lista final em um DataFrame tabular.
    Saída: pd.DataFrame consolidado com todas as métricas de todas as trilhas processadas.
    """
    resultados = []

    for arquivo in os.listdir(caminho_pasta_gpx):
        if arquivo.lower().endswith('.gpx'):
            caminho_completo = os.path.join(caminho_pasta_gpx, arquivo)

            try:
                resultado = analisar_trilha(caminho_completo)
                resultados.append(resultado)

            except Exception as erro:
                print(f"Erro ao processar {arquivo}: {erro}")

    return pd.DataFrame(resultados)
