# Classificação de Dificuldade via Clustering

## Objetivo
Descrever o processo de aprendizado de máquina utilizado para agrupar trilhas em níveis de dificuldade utilizando o algoritmo K-Means.

## Contexto no projeto
É o estágio final de inteligência do sistema, onde as métricas calculadas anteriormente são consolidadas para rotular as trilhas (Leve, Moderada, Pesada, Muito Pesada, Extrema).

## Fundamentação teórica
O agrupamento utiliza **K-Means Clustering**, um algoritmo de partição que minimiza a variância dentro dos clusters. Como as features possuem escalas diferentes (km, metros, minutos), a padronização (`StandardScaler`) é essencial para garantir pesos iguais na distância euclidiana.

## Requisitos
- Biblioteca `scikit-learn` para modelagem e pré-processamento.
- Dataset consolidade gerado pelas etapas anteriores.

## Estrutura técnica
Localizado em `src/clustering_dificuldade.py`.
- `classificar_dificuldade_kmeans`: Função principal que executa o pipeline de ML.

## Fluxo de funcionamento
1. Seleção de features: `intensidade_diaria`, `dias_trilha`, `indice_concentracao_esforco`.
2. Padronização dos dados (Z-score).
3. Execução do K-Means com centróides iniciais aleatórios (n=30).
4. Ordenação dos clusters baseada na soma dos centroides (para mapear 0 -> Leve, etc.).
5. Mapeamento de rótulos humanos aos IDs de cluster.

## Modelos de dados envolvidos
- **DataFrame Classificado**: Dataset original com colunas adicionais `cluster` e `dificuldade`.

## Variáveis científicas utilizadas
- **Intensidade Diária**: Métrica composta de tempo por km + ganho relativo.
- **Índice de Concentração de Esforço**: Desvio padrão dos ganhos diários / média.

## Endpoints ou CLI
N/A.

## Templates envolvidos
N/A.

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
- **K-Means (Unsupervised)**: k=3, 4 ou 5 (conforme configuração).

## Métricas de avaliação
- **Silhouette Coefficient**: Mede quão próximo um ponto está dos pontos de seu próprio cluster em relação aos pontos de outros clusters.

## Testes previstos
- Estabilidade dos clusters em diferentes execuções (Random State fixo).
- Sensibilidade à remoção de outliers de quilometragem.

## Referências acadêmicas
- PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **JMLR**, 2011.
- JAIN, A. K. Data clustering: 50 years beyond K-means. **Pattern Recognition Letters**, 2010.
