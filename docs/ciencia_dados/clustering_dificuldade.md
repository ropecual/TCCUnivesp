# Classificação de Dificuldade via Clustering

## Objetivo
Descrever o processo de aprendizado de máquina utilizado para agrupar trilhas em níveis de dificuldade utilizando uma abordagem comparativa entre **K-Means**, **Clustering Hierárquico** e **DBSCAN**.

## Contexto no projeto
É o estágio final de inteligência do sistema, onde as métricas calculadas anteriormente são consolidadas para rotular as trilhas (Leve, Moderada, Pesada, Muito Pesada, Extrema). A comparação entre algoritmos garante que a classificação seja robusta e validada por diferentes técnicas de agrupamento.

## Fundamentação teórica
O agrupamento utiliza três abordagens distintas de aprendizado não supervisionado:
1. **K-Means Clustering**: Algoritmo de partição que minimiza a variância dentro dos clusters. É o modelo principal para a rotulação em 5 níveis.
2. **Clustering Hierárquico (Agglomerative)**: Utiliza a métrica de Ward para construir uma hierarquia de clusters, validando a estrutura natural dos dados.
3. **DBSCAN**: Baseado em densidade, utilizado primariamente para identificar ruídos (outliers) e validar agrupamentos densos.

Como as features possuem escalas diferentes, a padronização (`StandardScaler`) é aplicada em todos os modelos.

## Requisitos
- Biblioteca `scikit-learn` para modelagem e pré-processamento.
- Dataset consolidado gerado pelas etapas anteriores.

## Estrutura técnica
Localizado em `src/clustering_dificuldade.py`.
- `classificar_dificuldade_kmeans`: Modelo principal de produção.
- `classificar_dificuldade_hierarquico`: Validação estrutural.
- `classificar_dificuldade_dbscan`: Detecção de anomalias e densidade.

## Fluxo de funcionamento
1. **Seleção de features**: `intensidade_diaria` (ID), `dias_trilha` e `indice_concentracao_esforco` (IC).
2. **Padronização**: Z-score para média zero e variância unitária.
3. **Execução Comparativa**:
   - K-Means com k=5.
   - Hierárquico com k=5 e ligação Ward.
   - DBSCAN para análise de densidade e ruído.
4. **Ordenação e Rotulação**: Clusters são ordenados pela soma dos IDs e ICs de seus centroides (ou pseudo-centroides) para garantir que 0 seja "Leve" e 4 seja "Extrema".

## Modelos de Machine Learning envolvidos
- **K-Means (Unsupervised)**: k=5 (Silhouette Score: ~0.442).
- **Agglomerative Clustering**: k=5.
- **DBSCAN**: eps=0.5, min_samples=3.

## Variáveis científicas utilizadas
- **Intensidade Diária (ID)**: Integra tempo estimado por km e métricas topográficas.
- **Índice de Concentração de Esforço (IC)**: IC = ID * (1 + ln(D)), onde D é a duração.

## Métricas de avaliação
- **Silhouette Coefficient**: Utilizado para medir a coesão e separação. O K-Means obteve 0.442, indicando uma estrutura sólida.
- **Análise de Ruído (DBSCAN)**: Identificação de trilhas atípicas que não se encaixam nos clusters padrão.

## Referências acadêmicas
- PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **JMLR**, 2011.
- JAIN, A. K. Data clustering: 50 years beyond K-means. **Pattern Recognition Letters**, 2010.
- MANTUANO, A.; BRUNO, F. Classification of hiking difficulty levels of accessible natural trails. **Sustainability**, 2025.
