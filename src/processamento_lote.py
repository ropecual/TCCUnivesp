import os
import pandas as pd

from src.analise_trilha import analisar_trilha


def processar_pasta_gpx(caminho_pasta_gpx: str) -> pd.DataFrame:
    """
    Processa todos os arquivos GPX de uma pasta,
    aplicando a análise completa em cada trilha.

    Retorna um DataFrame consolidado.
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
