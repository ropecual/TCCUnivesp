import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score


def classificar_dificuldade_kmeans(caminho_csv_entrada: str, caminho_csv_saida: str, n_clusters: int = 5) -> None:
    """
    Objetivo: Clusterizar e rotular as trilhas por nível de dificuldade percebida.
    Entrada: Caminho do CSV consolidado com as features científicas.
    Processamento: 
        1. Seleciona features-chave: Intensidade Diária (ID), Duração (Dias) e Índice de Concentração de Esforço (IC).
        2. Normaliza os dados (StandardScaler) para que quilometragens e scores tenham o mesmo peso.
        3. Treina o K-Means para encontrar padrões naturais de agrupamento.
        4. Calcula o Silhouette Score para validar a qualidade da segmentação (Ref. Monografia: 0.442).
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



def classificar_dificuldade_hierarquico(caminho_csv_entrada: str, caminho_csv_saida: str, n_clusters: int = 5) -> None:
    """
    Objetivo: Agrupamento hierárquico (Aglomerativo) para identificar níveis de dificuldade.
    Diferença: Constrói uma hierarquia de clusters de baixo para cima utilizando a ligação de Ward. 
    Serve como validação da estrutura natural de agrupamento dos dados (ID, Dias, IC).
    """
    df = pd.read_csv(caminho_csv_entrada)
    colunas = ['intensidade_diaria', 'dias_trilha', 'indice_concentracao_esforco']
    dados_cluster = df[colunas].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(dados_cluster)

    # Implementação Hierárquica
    hc = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    clusters = hc.fit_predict(X_scaled)
    df.loc[dados_cluster.index, 'cluster'] = clusters

    # Para ordenar os rótulos no Hierárquico, calculamos as médias de cada cluster (pseudo-centroides)
    pseudo_centroides = []
    for i in range(n_clusters):
        pseudo_centroides.append(X_scaled[clusters == i].mean(axis=0))
    
    scores = np.array(pseudo_centroides).sum(axis=1)
    ordem = scores.argsort()
    
    rotulos = ['Leve', 'Moderada', 'Pesada', 'Muito Pesada', 'Extrema']
    mapa = {ordem[i]: rotulos[i] for i in range(min(n_clusters, 5))}
    
    df['dificuldade'] = df['cluster'].map(mapa)
    
    if n_clusters > 1:
        silhouette = silhouette_score(X_scaled, clusters)
        print(f"Silhouette Score Hierárquico (k={n_clusters}): {silhouette:.3f}")

    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')



def classificar_dificuldade_dbscan(caminho_csv_entrada: str, caminho_csv_saida: str, eps: float = 0.5, min_samples: int = 5) -> None:
    """
    Objetivo: Identificar clusters por densidade e pontos anômalos (ruído).
    Diferença: Não exige definição prévia de k e identifica trilhas "fora do padrão" (outliers).
    Utilizado para validar a diversidade dos dados e detectar casos excepcionais (cluster -1).
    """
    df = pd.read_csv(caminho_csv_entrada)
    colunas = ['intensidade_diaria', 'dias_trilha', 'indice_concentracao_esforco']
    dados_cluster = df[colunas].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(dados_cluster)

    # Implementação DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(X_scaled)
    df.loc[dados_cluster.index, 'cluster'] = clusters

    # No DBSCAN, o rótulo -1 indica ruído/outlier
    n_clusters_encontrados = len(set(clusters)) - (1 if -1 in clusters else 0)
    
    if n_clusters_encontrados > 1:
        silhouette = silhouette_score(X_scaled, clusters)
        print(f"Silhouette Score DBSCAN (eps={eps}): {silhouette:.3f}")
    
    print(f"DBSCAN encontrou {n_clusters_encontrados} clusters e {list(clusters).count(-1)} pontos de ruído.")

    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')