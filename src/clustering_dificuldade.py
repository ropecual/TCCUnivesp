import pandas as pd
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
    com base em variáveis de esforço estimado derivadas
    da predição de tempo e características topográficas.

    Variáveis utilizadas:
    - tempo estimado por quilômetro (Tobler ou Naismith)
    - ganho de elevação por quilômetro
    - inclinação média
    """

    # ------------------------------------------------------------------
    # 1. Leitura dos dados
    # ------------------------------------------------------------------
    df = pd.read_csv(caminho_csv_entrada)

    # ------------------------------------------------------------------
    # 2. Seleção do tempo estimado mais adequado
    # Prioriza Tobler por ser contínuo em função da inclinação
    # ------------------------------------------------------------------
    df['tempo_estimado_min'] = df['tempo_tobler_min'].fillna(
        df['tempo_naismith_min']
    )

    # ------------------------------------------------------------------
    # 3. Engenharia de variáveis de esforço (NORMALIZADAS)
    # ------------------------------------------------------------------
    df['tempo_estimado_por_km'] = df['tempo_estimado_min'] / df['distancia_km']
    df['ganho_por_km'] = df['ganho_elevacao_m'] / df['distancia_km']

    variaveis_cluster = df[
        ['tempo_estimado_por_km', 'ganho_por_km', 'inclinacao_media_graus']
    ]

    # ------------------------------------------------------------------
    # 4. Normalização
    # ------------------------------------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(variaveis_cluster)

    # ------------------------------------------------------------------
    # 5. K-Means
    # ------------------------------------------------------------------
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=20
    )

    df['cluster'] = kmeans.fit_predict(X_scaled)

    # ------------------------------------------------------------------
    # 6. Avaliação
    # ------------------------------------------------------------------
    silhouette = silhouette_score(X_scaled, df['cluster'])
    print(f"Silhouette Score (k={n_clusters}): {silhouette:.3f}")

    # ------------------------------------------------------------------
    # 7. Interpretação semântica dos clusters
    # Ordenação por esforço estimado
    # ------------------------------------------------------------------
    resumo = (
        df
        .groupby('cluster')[
            ['tempo_estimado_por_km', 'ganho_por_km', 'inclinacao_media_graus']
        ]
        .mean()
        .reset_index()
    )

    resumo['indice_esforco'] = (
        resumo['tempo_estimado_por_km'] +
        resumo['ganho_por_km'] / 100 +
        resumo['inclinacao_media_graus']
    )

    resumo = resumo.sort_values('indice_esforco')

    rotulos = ['Leve', 'Moderada', 'Pesada']
    mapa_dificuldade = {
        cluster: rotulos[i]
        for i, cluster in enumerate(resumo['cluster'])
    }

    df['dificuldade'] = df['cluster'].map(mapa_dificuldade)

    # ------------------------------------------------------------------
    # 8. Salvando resultado
    # ------------------------------------------------------------------
    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')

    print("\nClassificação de dificuldade concluída.")
    print(df['dificuldade'].value_counts())
