# Classificação da Dificuldade de Trilhas de Trekking via Ciência de Dados

## 🎓 Contexto Acadêmico
Este repositório é parte integrante doprojeto de Trabalho de Conclusão de Curso (TCC) da **Universidade Virtual do Estado de São Paulo (UNIVESP)**. O sistema visa aplicar técnicas avançadas de Ciência de Dados e Machine Learning para resolver o desafio de padronização na classificação de dificuldade de trilhas de trekking, baseando-se em variáveis objetivas e modelos fisiológicos de esforço.

---

## 🔬 O Problema e Objetivos
A classificação de dificuldade de trilhas costuma ser subjetiva e variar drasticamente entre plataformas. Este projeto busca atender:
1. **Predição do Tempo de Execução**: Utilização de modelos matemáticos como a **Função de Caminhada de Tobler** e a **Regra de Naismith** para estimar o esforço temporal necessário.
2. **Análise Topográfica**: Processamento de dados GPX para extrair métricas de distância geodésica, ganho de elevação acumulado e inclinação média.
3. **Classificação Inteligente**: Aplicação de aprendizado não supervisionado (**K-Means Clustering**) para agrupar trilhas em níveis de dificuldade (Leve, Moderada, Pesada, Muito Pesada e Extrema) com base em métricas de intensidade e concentração de esforço.

---

## 🛠️ Arquitetura do Sistema
O projeto é estruturado como um pipeline modular em Python puro, garantindo escalabilidade para pesquisa científica:

- **Ingestão (`src/leitura_gpx.py`)**: Parser de arquivos GPX e normalização temporal.
- **Motor de Métricas (`src/metricas_trilha.py`)**: Extração de distância geodésica e desnível positivo.
- **Modelagem Preditiva (`src/modelos_tempo.py`)**: Implementação de algoritmos de cronometragem teórica.
- **Análise Consolidada (`src/analise_trilha.py`)**: Geração de features e scores de intensidade.
- **Inteligência Artificial (`src/clustering_dificuldade.py`)**: Segmentação de dados via Machine Learning.
- **Orquestração (`main.py`)**: Pipeline automatizado de processamento em lote.

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
- [Modelagem de Tempo](docs/ciencia_dados/modelagem_preditiva_tempo.py.md)
- [Clustering de Dificuldade](docs/ciencia_dados/clustering_dificuldade.md)

---

## ⚖️ Licença e Referências
*Projeto acadêmico desenvolvido sob os preceitos de Ciência Aberta.*
Principais referências:
- TOBLER, Waldo. *Three mountains algorithms*. (1993).
- NAISMITH, William. *Naismith's Rule*. (1892).