import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def classificar_dificuldade_kmeans(
    caminho_csv_entrada: str,
    caminho_csv_saida: str,
    n_clusters: int = 3
) -> None:
    """
    Classifica a dificuldade das trilhas utilizando K-Means,
    com base em variáveis de esforço relativo.

    Variáveis utilizadas:
    - tempo por quilômetro
    - ganho de elevação por quilômetro
    - inclinação média
    """

    # ------------------------------------------------------------------
    # 1. Leitura dos dados
    # ------------------------------------------------------------------
    df = pd.read_csv(caminho_csv_entrada)

    # ------------------------------------------------------------------
    # 2. Engenharia de variáveis (esforço relativo)
    # ------------------------------------------------------------------
    df['tempo_por_km'] = df['tempo_real_min'] / df['distancia_km']
    df['ganho_por_km'] = df['ganho_elevacao_m'] / df['distancia_km']
    df['velocidade_real_kmh'] = df['distancia_km'] / (df['tempo_real_min'] / 60)

    # Seleção das variáveis para clustering
    variaveis_cluster = df[
        ['tempo_por_km', 'ganho_por_km', 'inclinacao_media_graus']
    ]

    # ------------------------------------------------------------------
    # 3. Normalização (obrigatória para K-Means)
    # ------------------------------------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(variaveis_cluster)

    # ------------------------------------------------------------------
    # 4. Aplicação do K-Means
    # ------------------------------------------------------------------
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=20
    )

    df['cluster'] = kmeans.fit_predict(X_scaled)

    # ------------------------------------------------------------------
    # 5. Avaliação da qualidade do agrupamento
    # ------------------------------------------------------------------
    silhouette = silhouette_score(X_scaled, df['cluster'])
    print(f"Silhouette Score (k={n_clusters}): {silhouette:.3f}")

    # ------------------------------------------------------------------
    # 6. Interpretação dos clusters (ordenação por esforço)
    # ------------------------------------------------------------------
    # Calcula médias por cluster
    resumo = (
        df
        .groupby('cluster')[['tempo_por_km', 'ganho_por_km', 'inclinacao_media_graus']]
        .mean()
        .reset_index()
    )

    # Cria um índice de esforço simples para ordenar clusters
    resumo['indice_esforco'] = (
        resumo['tempo_por_km'] +
        resumo['ganho_por_km'] / 100 +
        resumo['inclinacao_media_graus']
    )

    resumo = resumo.sort_values('indice_esforco')

    # Mapeamento ordenado para rótulos semânticos
    rotulos = ['Leve', 'Moderada', 'Pesada']
    mapa_dificuldade = {
        cluster: rotulos[i]
        for i, cluster in enumerate(resumo['cluster'])
    }

    df['dificuldade'] = df['cluster'].map(mapa_dificuldade)

    # ------------------------------------------------------------------
    # 7. Salvando resultado final
    # ------------------------------------------------------------------
    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')

    print("\nClassificação de dificuldade concluída.")
    print("Distribuição das trilhas por dificuldade:")
    print(df['dificuldade'].value_counts())
