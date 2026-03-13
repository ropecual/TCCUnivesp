# Enriquecimento Geográfico de Dados

## Objetivo
Documentar a integração do pipeline com serviços de geocodificação reversa para identificação administrativa das trilhas.

## Contexto no projeto
Permite a filtragem e categorização das trilhas por Cidade, Estado ou País, enriquecendo a análise de dados com contexto regional.

## Fundamentação teórica
Utiliza o serviço **Nominatim** (baseado em OpenStreetMap) via biblioteca `geopy`. Implementa estratégias de `RateLimiting` para respeitar as políticas de uso gratuito de serviços acadêmicos.

## Requisitos
- Biblioteca `geopy`.
- Conexão TLS/SSL ativa.
- Respeito ao delay mínimo de 1-5 segundos entre chamadas.

## Estrutura técnica
Localizado em `src/enriquecimento_geografico.py`.
- `enriquecer_localizacao`: Função orquestradora com cache em memória.

## Fluxo de funcionamento
1. Leitura do CSV de análise.
2. Identificação da coordenada de início da trilha (ponto 0).
3. Consulta ao cache local para evitar chamadas redundantes.
4. Chamada à API Nominatim via Geopy.
5. Parser do dicionário de endereço (JSON).
6. Atualização do CSV com novas colunas.

## Modelos de dados envolvidos
- **Dicionário de Endereço**: Estrutura `raw` retornada pelo Nominatim.

## Variáveis científicas utilizadas
- Coordenadas geográficas WGS84 (Lat/Lon).

## Endpoints ou CLI
Chamada via `main.py` com interação do usuário (prompt S/N).

## Templates envolvidos
N/A.

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
N/A.

## Métricas de avaliação
- Taxa de sucesso de geocodificação.
- Latência média por requisição.

## Testes previstos
- Tratamento de `Timeouts` e `ServiceUnavailable`.
- Validação de trilhas em regiões remotas onde o endereço administrativo pode ser nulo ou incompleto.

## Referências acadêmicas
- OPENSTREETMAP FOUNDATION. **Nominatim Usage Policy**. 2023.
