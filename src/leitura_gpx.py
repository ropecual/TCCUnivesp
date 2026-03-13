import gpxpy
import pandas as pd


def ler_gpx(caminho_gpx: str) -> pd.DataFrame:
    """
    Objetivo: Extrair e normalizar dados brutos de arquivos GPX.
    Entrada: String com o caminho do arquivo .gpx.
    Processamento: 
        1. Parseia o XML usando gpxpy.
        2. Navega pela hierarquia Tracks -> Segments -> Points.
        3. Filtra apenas pontos com Latitude, Longitude e Elevação válidas.
        4. Cria um DataFrame Pandas e converte timestamps para UTC.
        5. Ordena os pontos cronologicamente para garantir integridade física da trilha.
    Saída: pd.DataFrame com colunas ['latitude', 'longitude', 'altitude_m', 'time'].
    """
    with open(caminho_gpx, 'r', encoding='utf-8') as arquivo:
        gpx = gpxpy.parse(arquivo)

    pontos = []

    for trilha in gpx.tracks:
        for segmento in trilha.segments:
            for ponto in segmento.points:
                if (
                    ponto.latitude is None or
                    ponto.longitude is None or
                    ponto.elevation is None
                ):
                    continue

                pontos.append({
                    'latitude': ponto.latitude,
                    'longitude': ponto.longitude,
                    'altitude_m': ponto.elevation,
                    'time': ponto.time
                })

    df = pd.DataFrame(pontos)

    if df.empty:
        raise ValueError(f"GPX sem pontos válidos: {caminho_gpx}")

    # ------------------------------------------------------------------
    # Normalização temporal
    # ------------------------------------------------------------------
    df['time'] = pd.to_datetime(df['time'], utc=True, errors='coerce')
    df = df.sort_values('time').reset_index(drop=True)

    return df


def calcular_tempo_total_minutos(dados: pd.DataFrame) -> float:
    """
    Objetivo: Calcular a duração total da atividade (tempo de relógio).
    Entrada: pd.DataFrame contendo a coluna 'time' com objetos datetime.
    Processamento: 
        1. Verifica a existência da coluna 'time'.
        2. Extrai o timestamp inicial (primeiro ponto) e o final (último ponto).
        3. Calcula a diferença temporal absoluta.
    Saída: Float representando o tempo total em minutos. Retorna None se não houver dados temporais suficientes.
    """
    if 'time' not in dados.columns:
        return None

    tempos_validos = dados['time'].dropna()

    if len(tempos_validos) < 2:
        return None

    inicio = tempos_validos.iloc[0]
    fim = tempos_validos.iloc[-1]

    return (fim - inicio).total_seconds() / 60
