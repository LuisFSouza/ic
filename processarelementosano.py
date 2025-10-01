import pandas as pd

dfdados = pd.read_csv('./elementos_por_ano_bruto.csv')
dfretirar = pd.read_csv('./elementos_retirar.csv')

dfjuncao = dfdados.merge(dfretirar, how='left', left_on=['symbol', 'yearpublished'], right_on=['simbolo', 'ano'])
dfjuncao['erros'] = dfjuncao['erros'].fillna(0).astype(int)
dfjuncao['qtdd'] = dfjuncao['qtdd'].astype(int) - dfjuncao['erros']

dfsalvar = dfjuncao[dfjuncao['qtdd'] > 0]
dfsalvar = dfsalvar[["symbol","yearpublished","qtdd"]]

dfsalvar.to_csv('./elementos_por_ano_final.csv', index=False)