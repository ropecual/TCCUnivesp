import numpy as np

def estimar_tempo_naismith_min(distancia_km: float, ganho_elevacao_m: float) -> float:
    """
    Objetivo: Estimar o tempo de percurso usando a Regra de Naismith (1892).
    Entrada: Distância em km e Ganho de elevação em metros.
    Mecânica: 
        - Velocidade base: 5 km/h (12 min/km).
        - Penalidade: +1 min para cada 10 metros de subida (60 min / 600m).
    Saída: Float representando o tempo estimado em minutos.
    """
    tempo_horas = (distancia_km / 5) + (ganho_elevacao_m / 600)
    return tempo_horas * 60





def estimar_tempo_tobler_min(distancia_km: float, inclinacao_media_graus: float) -> float:
    """
    Objetivo: Estimar o tempo baseado na fisiologia de deslocamento (Tobler's Hiking Function).
    Entrada: Distância em km e Inclinação média em graus.
    Mecânica: 
        - Calcula a velocidade exponencial: V = 6 * exp(-3.5 * |tan(theta) + 0.05|).
        - Aplica limite mínimo de 0.1 km/h para evitar divisões por zero ou valores absurdos.
    Saída: Float representando o tempo em minutos baseado na dificuldade do terreno.
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
