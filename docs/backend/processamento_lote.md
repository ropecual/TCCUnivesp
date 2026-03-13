# Orquestração e Processamento em Lote

## Objetivo
Documentar o fluxo de execução principal do sistema e a capacidade de processamento em massa de dados GPX.

## Contexto no projeto
Componente de interface com o usuário e automação, responsável por unir todos os módulos de ciência de dados em um pipeline executável.

## Fundamentação teórica
O processamento segue o padrão de **Processamento Orientado a Arquivos**, comum em ambientes de pesquisa onde os dados são coletados de forma assíncrona e processados periodicamente em lote para atualização de modelos.

## Requisitos
- Estrutura de pastas `dados/gpx/` preenchida com arquivos `.gpx`.
- Python 3.10+ configurado no PATH.

## Estrutura técnica
- `main.py`: Ponto de entrada (Entry point).
- `src/processamento_lote.py`: Lógica de varredura de diretórios e tratamento de exceções.

## Fluxo de funcionamento
1. Usuário executa `python main.py`.
2. O sistema lista todos os arquivos na pasta de dados.
3. Para cada arquivo, executa-se `analisar_trilha`.
4. Captura eventuais erros em arquivos corrompidos sem interromper o pipeline.
5. Solicita decisão sobre enriquecimento online.
6. Dispara o clustering final.

## Modelos de dados envolvidos
N/A.

## Variáveis científicas utilizadas
N/A (Orquestração funcional).

## Endpoints ou CLI
Execução manual via terminal.

## Templates envolvidos
N/A.

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
Aciona o modelo KMeans de `clustering_dificuldade.py`.

## Métricas de avaliação
- Tempo total de processamento do lote.
- Porcentagem de arquivos processados com sucesso vs. falhas.

## Testes previstos
- Execução com pasta vazia.
- Execução com arquivos de formatos diversos (não-GPX).

## Referências acadêmicas
- UNIVESP. **Guia de Desenvolvimento de Sistemas em Python para TCC**.
