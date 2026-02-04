import time
import pandas as pd

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def enriquecer_localizacao(
    caminho_csv_entrada: str,
    caminho_csv_saida: str,
    atraso_minimo_segundos: int = 5
) -> None:
    """
    Realiza enriquecimento geográfico (cidade, estado, país)
    a partir das coordenadas iniciais das trilhas.

    Implementação conservadora, tolerante a falhas e adequada
    para uso acadêmico com o serviço Nominatim.
    """

    df = pd.read_csv(caminho_csv_entrada)

    geolocator = Nominatim(user_agent="tcc_univesp_geocoding")

    reverse = RateLimiter(
        geolocator.reverse,
        min_delay_seconds=atraso_minimo_segundos,
        error_wait_seconds=atraso_minimo_segundos * 2,
        max_retries=2,
        swallow_exceptions=True
    )

    # Cache simples para evitar chamadas repetidas
    cache = {}

    cidades = []
    estados = []
    paises = []

    print("Iniciando enriquecimento geográfico ...\n")

    for idx, linha in df.iterrows():
        lat = round(linha['latitude_inicio'], 6)
        lon = round(linha['longitude_inicio'], 6)
        chave = (lat, lon)

        if chave in cache:
            cidade, estado, pais = cache[chave]
        else:
            location = reverse((lat, lon), language='pt', timeout=10)

            if location and 'address' in location.raw:
                endereco = location.raw['address']

                cidade = (
                    endereco.get('city')
                    or endereco.get('town')
                    or endereco.get('village')
                    or endereco.get('municipality')
                )
                estado = endereco.get('state')
                pais = endereco.get('country')
            else:
                cidade = None
                estado = None
                pais = None

            cache[chave] = (cidade, estado, pais)

            # Pausa adicional de segurança
            time.sleep(atraso_minimo_segundos)

        cidades.append(cidade)
        estados.append(estado)
        paises.append(pais)

        print(
            f"[{idx + 1}/{len(df)}] "
            f"({lat}, {lon}) → {cidade}, {estado}, {pais}"
        )

    df['cidade'] = cidades
    df['estado'] = estados
    df['pais'] = paises

    df.to_csv(caminho_csv_saida, index=False, encoding='utf-8')

    print(f"\n✔ Enriquecimento concluído.")
    print(f"✔ Arquivo salvo em: {caminho_csv_saida}")
