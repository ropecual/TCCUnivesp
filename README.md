# Classificação da Dificuldade de Trilhas de Trekking via Ciência de Dados

## 🎓 Contexto Acadêmico
Este repositório é parte integrante doprojeto de Trabalho de Conclusão de Curso (TCC) da **Universidade Virtual do Estado de São Paulo (UNIVESP)**. O sistema visa aplicar técnicas avançadas de Ciência de Dados para resolver o desafio de padronização na classificação de dificuldade de trilhas de trekking, baseando-se em variáveis objetivas e modelos fisiológicos de esforço.

---

## 🔬 O Problema e Objetivos
A classificação de dificuldade de trilhas costuma ser subjetiva e variar drasticamente entre plataformas. Este projeto busca atender:
1. **Predição do Tempo de Execução**: Utilização de modelos matemáticos como a **Função de Caminhada de Tobler** e a **Regra de Naismith** para estimar o esforço temporal necessário.
2. **Análise Topográfica**: Processamento de dados GPX para extrair métricas de distância geodésica, ganho de elevação acumulado e inclinação média.
3. **Classificação Inteligente**: Abordagem comparativa de aprendizado não supervisionado utilizando **K-Means**, **Clustering Hierárquico** e **DBSCAN** para agrupar trilhas em níveis de dificuldade (Leve a Extrema) e detectar anomalias, com validação via Silhouette Score.

---

## 🛠️ Arquitetura do Sistema
O projeto é estruturado como um pipeline modular em Python, integrando geoprocessamento e machine learning:

- **Processamento em Lote (`src/processamento_lote.py`)**: Coordena a leitura massiva de arquivos GPX.
- **Ingestão (`src/leitura_gpx.py`)**: Parser de arquivos GPX e extração de coordenadas/tempo.
- **Motor de Métricas (`src/metricas_trilha.py`)**: Cálculo de distância geodésica, ganho de elevação e inclinação.
- **Enriquecimento (`src/enriquecimento_geografico.py`)**: Integração com API Nominatim para localização reversa.
- **Modelagem Preditiva (`src/modelos_tempo.py`)**: Estimativa teórica baseada em Tobler e Naismith.
- **Análise Consolidada (`src/analise_trilha.py`)**: Geração de features científicas (ID e IC).
- **Clustering Comparativo (`src/clustering_dificuldade.py`)**: Implementação de K-Means, Hierárquico e DBSCAN.
- **Orquestração (`main.py`)**: Fluxo principal de execução do pipeline.

---

## 🚦 Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Posicione seus arquivos GPX em `dados/gpx/`.
3. Execute o script principal: `python main.py`
4. Os resultados (CSV) serão gerados em `dados/resultados/`, incluindo a classificação final de dificuldade.

---

## 📚 Documentação Técnica
Para detalhes aprofundados sobre a fundamentação teórica e o funcionamento interno de cada módulo, consulte a pasta `docs/`:
- [Visão Geral da Arquitetura](docs/arquitetura/visao_geral.md)
- [Modelagem de Tempo](docs/ciencia_dados/modelagem_preditiva_tempo.md)
- [Clustering de Dificuldade](docs/ciencia_dados/clustering_dificuldade.md)

---

## ⚖️ Licença e Referências
*Projeto acadêmico desenvolvido sob os preceitos de Ciência Aberta.*
Principais referências:
- TOBLER, Waldo. *Three mountains algorithms*. (1993).
- NAISMITH, William. *Naismith's Rule*. (1892).