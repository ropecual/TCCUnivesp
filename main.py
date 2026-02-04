from src.processamento_lote import processar_pasta_gpx

# Caminho da pasta com os GPX
pasta_gpx = 'dados/gpx'

# Processamento em lote
df_resultados = processar_pasta_gpx(pasta_gpx)

# Exibir resultados
print(df_resultados)

# Salvar tabela final
df_resultados.to_csv(
    'dados/resultados/analise_trilhas.csv',
    index=False,
    encoding='utf-8'
)
