# Visão Geral da Arquitetura do Sistema

## Objetivo
Descrever a estrutura macroscópica do pipeline de processamento de dados geográficos para classificação de dificuldade de trilhas de trekking.

## Contexto no projeto
Este documento serve como o mapa central para desenvolvedores e pesquisadores entenderem como os dados fluem desde a entrada (arquivos GPX) até a saída final (CSV classificado com níveis de dificuldade).

## Fundamentação teórica
A arquitetura baseia-se no conceito de **Pipeline de Ciência de Dados**, composto pelas etapas de Ingestão, Processamento/Engenharia de Features, Enriquecimento e Modelagem Preditiva. Utiliza-se a integração de dados geoespaciais e algoritmos de aprendizado não supervisionado.

## Requisitos
- Ambiente Python 3.10+
- Bibliotecas: `pandas`, `gpxpy`, `geopy`, `scikit-learn`, `numpy`
- Acesso à internet (para enriquecimento via Nominatim)

## Estrutura técnica
O sistema é estruturado em módulos Python puros dentro do diretório `src/`, orquestrados por um script principal `main.py`.
- `leitura_gpx.py`: Parser de dados brutos.
- `metricas_trilha.py`: Motor de cálculo geométrico e físico.
- `analise_trilha.py`: Agregador de métricas e gerador de scores.
- `modelos_tempo.py`: Implementação de fórmulas de estimativa de esforço.
- `clustering_dificuldade.py`: Engine de Machine Learning.

## Fluxo de funcionamento
1. **Ingestão**: Varredura da pasta `dados/gpx/`.
2. **Análise Individual**: Cálculo de distância, ganho de elevação e tempo estimado.
3. **Consolidação**: Geração de um dataset consolidado em CSV.
4. **Enriquecimento**: (Opcional) Adição de dados de localização via API.
5. **Classificação**: Aplicação de K-Means para segmentação em níveis (Leve a Extrema).

## Modelos de dados envolvidos
- **DataFrame de Pontos**: Estrutura temporária com lat, lon, alt e tempo.
- **CSV de Resultados**: Dataset com colunas de métricas (`distancia_km`, `ganho_elevacao_m`, `intensidade_diaria`, etc.).

## Variáveis científicas utilizadas
- Latitude, Longitude, Altitude (m)
- Timestamp (UTC)
- Distância Geodésica
- Inclinação Média

## Endpoints ou CLI
A interação ocorre via Interface de Linha de Comando (CLI) através da execução de `python main.py`.

## Templates envolvidos
N/A (Projeto sem interface web/Django).

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
- **K-Means Clustering**: Para agrupamento das trilhas com base no esforço e morfologia.

## Métricas de avaliação
- **Silhouette Score**: Para verificar a coesão e separação dos clusters de dificuldade.

## Testes previstos
- Validação de integridade de arquivos GPX.
- Testes unitários para as fórmulas de Tobler e Naismith.
- Verificação de convergência do K-Means.

## Referências acadêmicas
- TOBLER, W. Three mountains algorithms. **Machine Graphics and Vision**, 1993.
- NAISMITH, W. Naismith's Rule. **Scottish Mountaineering Club Journal**, 1892.
