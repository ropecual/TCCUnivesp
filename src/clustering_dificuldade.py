import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def classificar_dificuldade_kmeans(caminho_csv_entrada: str, caminho_csv_saida: str, n_clusters: int = 5) -> None:
    """
    Objetivo: Clusterizar e rotular as trilhas por nível de dificuldade percebida.
    Entrada: Caminho do CSV consolidado com as features científicas.
    Processamento: 
        1. Seleciona features-chave: Intensidade, Duração (Dias) e Concentração de Esforço.
        2. Normaliza os dados (StandardScaler) para que quilometragens e scores tenham o mesmo peso.
        3. Treina o K-Means para encontrar padrões naturais de agrupamento.
        4. Calcula o Silhouette Score para validar a qualidade da segmentação.
        5. Lógica de Negócio: Ordena os clusters pela "severidade" do centroide e mapeia nomes (Leve -> Extrema).
    Saída: Salva um novo CSV com as colunas 'cluster' e 'dificuldade'.
    """

    df = pd.read_csv(caminho_csv_entrada)

    colunas = [
        'intensidade_diaria',
        'dias_trilha',
        'indice_concentracao_esforco'
    ]

    dados_cluster = df[colunas].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(dados_cluster)

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=30
    )

    clusters = kmeans.fit_predict(X_scaled)

    df.loc[dados_cluster.index, 'cluster'] = clusters

    if n_clusters > 1:
        silhouette = silhouette_score(X_scaled, clusters)
        print(f"Silhouette Score (k={n_clusters}): {silhouette:.3f}")

    # ------------------------------------------------------------
    # ORDENAÇÃO CORRETA DOS CLUSTERS
    # Usa centroide já na escala padronizada
    # ------------------------------------------------------------

    centroides = kmeans.cluster_centers_

    scores = centroides.sum(axis=1)

    ordem = scores.argsort()

    if n_clusters == 5:
        rotulos = [
            'Leve',
            'Moderada',
            'Pesada',
            'Muito Pesada',
            'Extrema'
        ]
    elif n_clusters == 4:
        rotulos = [
            'Leve',
            'Moderada',
            'Pesada',
            'Extrema'
        ]
    elif n_clusters == 3:
        rotulos = [
            'Leve',
            'Moderada',
            'Pesada'
        ]
    else:
        raise ValueError("Número de clusters não suportado.")

    mapa = {
        ordem[i]: rotulos[i]
        for i in range(n_clusters)
    }

    df['dificuldade'] = df['cluster'].map(mapa)

    df.to_csv(
        caminho_csv_saida,
        index=False,
        encoding='utf-8'
    )

    print("\nClassificação concluída.")
    print(df['dificuldade'].value_counts())
