import numpy as np

def estimar_tempo_naismith_min(distancia_km: float, ganho_elevacao_m: float) -> float:
    """
    Estima o tempo de execução da trilha (em minutos) utilizando a Regra de Naismith.

    Premissas:
    - 1 hora para cada 5 km de distância horizontal
    - 1 hora adicional para cada 600 m de ganho de elevação positivo
    """
    tempo_horas = (distancia_km / 5) + (ganho_elevacao_m / 600)
    return tempo_horas * 60





def estimar_tempo_tobler_min(distancia_km: float, inclinacao_media_graus: float) -> float:
    """
    Estima o tempo de execução da trilha (em minutos) utilizando a Função de Caminhada de Tobler.

    A inclinação média deve ser fornecida em graus.


    A Função de Caminhada de Tobler foi utilizada para estimar o tempo de execução a partir da relação exponencial
    entre velocidade de deslocamento e inclinação do terreno.
    """
    # Conversão de graus para radianos
    inclinacao_rad = np.radians(inclinacao_media_graus)

    # Velocidade segundo Tobler (km/h)
    velocidade_kmh = 6 * np.exp(-3.5 * np.abs(np.tan(inclinacao_rad) + 0.05))

    # Evita velocidades irrealistas
    velocidade_kmh = max(velocidade_kmh, 0.1)

    # Tempo = distância / velocidade
    tempo_horas = distancia_km / velocidade_kmh
    return tempo_horas * 60
