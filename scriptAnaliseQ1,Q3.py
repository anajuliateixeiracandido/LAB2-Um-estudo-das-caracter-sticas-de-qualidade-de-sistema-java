import pandas as pd
import numpy as np

df = pd.read_csv('ck_summary.csv')

bins_pop = [3000, 10000, 50000, np.inf]
labels_pop = ['Populares', 'Muito populares', 'Extremamente populares']
df['popularidade'] = pd.cut(df['stars'], bins=bins_pop, labels=labels_pop)

bins_ativ = [-1, 0, 10, 50, np.inf]
labels_ativ = ['Inativos', 'Baixa atividade', 'Média atividade', 'Alta atividade']
df['atividade'] = pd.cut(df['num_releases'], bins=bins_ativ, labels=labels_ativ)

metricas = ['cbo_avg', 'dit_avg', 'lcom_avg']

estat_pop = df.groupby('popularidade', observed=True)[metricas].agg(['mean', 'median', 'std'])
estat_ativ = df.groupby('atividade', observed=True)[metricas].agg(['mean', 'median', 'std'])

print(estat_pop)
print(estat_ativ)

estat_pop.to_csv('estatisticas_popularidade.csv')
estat_ativ.to_csv('estatisticas_atividade.csv')