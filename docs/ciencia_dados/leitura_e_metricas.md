# Leitura de Dados e Cálculo de Métricas

## Objetivo
Documentar os procedimentos de parsing de arquivos GPX e a extração de métricas fundamentais de trilhas utilizando geometria geodésica.

## Contexto no projeto
Este componente representa a fundação do pipeline, transformando arquivos XML (GPX) em estruturas de dados tabulares (Pandas) preparadas para análise estatística.

## Fundamentação teórica
A extração de métricas utiliza a **Distância Geodésica** (fórmula de Vincenty ou Haversine via `geopy`) para precisão em superfícies elipsoidais. O cálculo de ganho de elevação aplica filtros de ruído para mitigar as imprecisões inerentes ao GPS e modelos digitais de elevação (DEM).

## Requisitos
- Biblioteca `gpxpy` para parsing de XML.
- Biblioteca `geopy` para cálculos espaciais.
- Arquivos GPX com trilhas válidas e tracks/segments.

## Estrutura técnica
Implementado nos módulos:
- `src/leitura_gpx.py`: Funções `ler_gpx` e `calcular_tempo_total_minutos`.
- `src/metricas_trilha.py`: Funções `calcular_distancia_total_km` e `calcular_ganho_elevacao_m`.

## Fluxo de funcionamento
1. Abertura do arquivo GPX.
2. Iteração sobre tracks, segmentos e pontos.
3. Extração de latitude, longitude e elevação.
4. Normalização temporal (UTC).
5. Cálculo acumulado de distâncias horizantais e verticais.

## Modelos de dados envolvidos
- **DataFrame de Pontos**: Colunas `latitude`, `longitude`, `altitude_m`, `time`.

## Variáveis científicas utilizadas
- `distancia_total`: Soma das distâncias entre pontos consecutivos.
- `ganho_elevacao`: Soma acumulada de deltas positivos superiores a um limiar de ruído (3m default).
- `tempo_ativo`: Tempo de deslocamento dentro de faixas de velocidade plausíveis (0.5 - 7.0 km/h).

## Endpoints ou CLI
N/A - Chamadas internas via API Python.

## Templates envolvidos
N/A.

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
N/A nesta etapa (Pré-processamento).

## Métricas de avaliação
- Erro acumulado na distância (comparação com software comercial como Garmin/Strava).
- Sensibilidade ao limiar de ruído vertical (`delta_min_m`).

## Testes previstos
- Testes com GPX sem timestamps (fallback para cálculo de distância apenas).
- Testes com saltos de GPS para validar filtros de velocidade.

## Referências acadêmicas
- WIKILOC. **Avaliação de Trilhas Ecológicas**. 2024.
- UNIVESP. **Metodologias de Coleta de Dados Geoespaciais**.
