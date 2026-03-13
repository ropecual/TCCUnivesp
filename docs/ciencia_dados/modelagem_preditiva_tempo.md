# Modelagem Preditiva de Tempo de Execução

## Objetivo
Documentar a implementação das funções clássicas de estimativa de tempo de caminhada (Tobler e Naismith) aplicadas à Ciência de Dados do projeto.

## Contexto no projeto
Essas métricas são utilizadas para normalizar o esforço físico necessário para completar uma trilha, independentemente da distância absoluta, servindo como features para o clustering de dificuldade.

## Fundamentação teórica
- **Função de Caminhada de Tobler**: Relação exponencial entre a inclinação do terreno e a velocidade de caminhada ($v = 6 \cdot e^{-3.5 \cdot |\tan(\theta) + 0.05|}$).
- **Regra de Naismith**: Estimativa empírica que adiciona tempo fixo para cada quilômetro horizontal e para cada metro de ganho vertical.

## Requisitos
- `numpy` para cálculos matemáticos e funções exponenciais/trigonométricas.

## Estrutura técnica
Localizado em `src/modelos_tempo.py`.
- `estimar_tempo_tobler_min`: Implementação da função exponencial.
- `estimar_tempo_naismith_min`: Implementação da regra linear de 5km/h e 600m/h.

## Fluxo de funcionamento
1. Recebe distância horizontal e inclinação/ganho de elevação.
2. Calcula a velocidade teórica média.
3. Retorna o tempo total estimado em minutos.

## Modelos de dados envolvidos
Parâmetros escalares (`float`).

## Variáveis científicas utilizadas
- Inclinação ($\theta$) em graus e radianos.
- Velocidade Teórica ($v$) em km/h.
- Delta de Elevação ($h$) em metros.

## Endpoints ou CLI
N/A.

## Templates envolvidos
N/A.

## Scripts JS envolvidos
N/A.

## Modelos de Machine Learning envolvidos
N/A (Modelos matemáticos determinísticos).

## Métricas de avaliação
- Correlação entre tempo predito e tempo real coletado no GPX.
- Resíduos da estimativa de Tobler em terrenos de alta inclinação (> 15º).

## Testes previstos
- Validação de saída para inclinação zero (velocidade máxima teórica de aprox. 5.1 km/h).
- Validação para descidas (verificar o "ombro" da curva de Tobler em -5º).

## Referências acadêmicas
- TOBLER, Waldo. **Three mountains algorithms**. 1993.
- NAISMITH, William. **Scottish Mountaineering Club Journal**. 1892.
