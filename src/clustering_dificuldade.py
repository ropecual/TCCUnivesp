import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def classificar_dificuldade_kmeans(
    caminho_csv_entrada: str,
    caminho_csv_saida: str,
    n_clusters: int = 4
) -> None:
    """
    Classificação da dificuldade de trilhas a partir de esforço diário
    e carga acumulada (multi-day).

    Escopo:
    - dificuldade topográfica e cinemática
    """

    # ------------------------------------------------------------
    # 1. Leitura
    # ------------------------------------------------------------
    df = pd.read_csv(caminho_csv_entrada)

    # ------------------------------------------------------------
    # 2. Tempo estimado de referência
    # ------------------------------------------------------------
    df['tempo_estimado_min'] = df['tempo_tobler_min'].fillna(
        df['tempo_naismith_min']
    )

    # ------------------------------------------------------------
    # 3. Engenharia de variáveis
    # ------------------------------------------------------------
    df['tempo_estimado_por_km_dia'] = (
        df['tempo_estimado_min'] / df['distancia_por_dia_km']
    )

    df['ganho_por_km'] = df['ganho_elevacao_m'] / df['distancia_km']

    # CARGA ACUMULADA
    df['carga_multiday'] = (
            df['dias_trilha'] * df['tempo_estimado_por_km_dia']
    )

    variaveis_cluster = df[
        [
            'tempo_estimado_por_km_dia',
            'ganho_por_km',
            'inclinacao_media_graus',
            'carga_multiday'
        ]
    ].dropna()

    # ------------------------------------------------------------
    # 4. Normalização
    # ------------------------------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(variaveis_cluster)

    # ------------------------------------------------------------
    # 5. K-Means
    # ------------------------------------------------------------
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=30
    )

    df.loc[variaveis_cluster.index, 'cluster'] = (
        kmeans.fit_predict(X_scaled)
    )

    # ------------------------------------------------------------
    # 6. Avaliação
    # ------------------------------------------------------------
    if n_clusters > 1:
        silhouette = silhouette_score(
            X_scaled,
            df.loc[variaveis_cluster.index, 'cluster']
        )
        print(f"Silhouette Score (k={n_clusters}): {silhouette:.3f}")

    # ------------------------------------------------------------
    # 7. Interpretação semântica
    # ------------------------------------------------------------
    resumo = (
        df
        .groupby('cluster')[
            [
                'tempo_estimado_por_km_dia',
                'ganho_por_km',
                'inclinacao_media_graus',
                'carga_multiday'
            ]
        ]
        .mean()
        .reset_index()
    )

    resumo['indice_esforco'] = (
        resumo['tempo_estimado_por_km_dia']
        + resumo['ganho_por_km'] / 100
        + resumo['inclinacao_media_graus']
        + resumo['carga_multiday'] / 10
    )

    resumo = resumo.sort_values('indice_esforco')

    if n_clusters == 4:
        rotulos = ['Leve', 'Moderada', 'Pesada', 'Extrema']
    elif n_clusters == 3:
        rotulos = ['Leve', 'Moderada', 'Pesada']
    else:
        rotulos = ['Leve', 'Pesada']

    mapa_dificuldade = {
        cluster: rotulos[i]
        for i, cluster in enumerate(resumo['cluster'])
    }

    df['dificuldade'] = df['cluster'].map(mapa_dificuldade)

    # ------------------------------------------------------------
    # 8. Persistência
    # ------------------------------------------------------------
    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')

    print("\nClassificação de dificuldade concluída.")
    print(df['dificuldade'].value_counts())
