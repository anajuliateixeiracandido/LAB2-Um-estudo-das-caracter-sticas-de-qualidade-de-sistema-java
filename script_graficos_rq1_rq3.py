import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 8)
plt.style.use('seaborn-v0_8-whitegrid')

rq01_data = {
    'Popularidade': ['Populares', 'Muito populares', 'Extremamente populares'],
    'CBO_mean': [5.40, 5.33, 3.03],
    'DIT_mean': [1.47, 1.45, 1.19],
    'LCOM_mean': [54.52, 343.80, 102.71]
}
rq01_df = pd.DataFrame(rq01_data)

rq03_data = {
    'Atividade': ['Inativos', 'Baixa atividade', 'Média atividade', 'Alta atividade'],
    'CBO_mean': [4.52, 5.15, 5.63, 6.41],
    'DIT_mean': [1.38, 1.47, 1.50, 1.52],
    'LCOM_mean': [218.96, 66.95, 69.10, 77.69]
}
rq03_df = pd.DataFrame(rq03_data)

def validar_df(df, cols):
    for col in cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Coluna {col} não é numérica.")
        if df[col].isnull().any():
            raise ValueError(f"Coluna {col} possui valores nulos.")

def plot_rq01(df):
    validar_df(df, ['CBO_mean', 'DIT_mean', 'LCOM_mean'])
    categorias = df['Popularidade']
    x = np.arange(len(categorias))
    width = 0.25
    fig, ax1 = plt.subplots(figsize=(12,8))
    bars1 = ax1.bar(x - width, df['CBO_mean'], width, label='CBO', color='#1f77b4')
    bars2 = ax1.bar(x, df['DIT_mean'], width, label='DIT', color='#2ca02c')
    ax2 = ax1.twinx()
    bars3 = ax2.bar(x + width, df['LCOM_mean'], width, label='LCOM', color='#ff7f0e', alpha=0.85)
    for bar in bars1:
        ax1.annotate(f'{bar.get_height():.2f}',
                     xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=11)
    for bar in bars2:
        ax1.annotate(f'{bar.get_height():.2f}',
                     xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=11)
    for bar in bars3:
        ax2.annotate(f'{bar.get_height():.2f}',
                     xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=11)
    ax1.set_title('RQ01: Relação entre Popularidade e Qualidade de Código\nMétricas CBO, DIT e LCOM por nível de popularidade', fontsize=16, weight='bold', pad=20)
    ax1.set_xlabel('Popularidade', fontsize=14)
    ax1.set_ylabel('CBO / DIT', fontsize=14)
    ax2.set_ylabel('LCOM', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categorias, fontsize=13)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax2.grid(False)
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper right', fontsize=13)
    plt.tight_layout()
    plt.savefig('imagens/rq01_popularidade_vs_qualidade.png', dpi=300)
    plt.savefig('imagens/rq01_popularidade_vs_qualidade.pdf', dpi=300)
    plt.close()

def plot_rq03(df):
    validar_df(df, ['CBO_mean', 'DIT_mean', 'LCOM_mean'])
    x = np.arange(len(df['Atividade']))
    fig, ax1 = plt.subplots(figsize=(12,8))
    ax1.plot(x, df['CBO_mean'], label='CBO', color='#1f77b4', marker='o', linestyle='-', linewidth=2, markersize=8)
    ax1.plot(x, df['DIT_mean'], label='DIT', color='#2ca02c', marker='s', linestyle='--', linewidth=2, markersize=8)
    ax2 = ax1.twinx()
    ax2.plot(x, df['LCOM_mean'], label='LCOM', color='#ff7f0e', marker='^', linestyle=':', linewidth=2, markersize=8)
    for i, val in enumerate(df['CBO_mean']):
        ax1.annotate(f'{val:.2f}', (x[i], val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=11)
    for i, val in enumerate(df['DIT_mean']):
        ax1.annotate(f'{val:.2f}', (x[i], val), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=11)
    for i, val in enumerate(df['LCOM_mean']):
        ax2.annotate(f'{val:.2f}', (x[i], val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=11)
    ax1.set_title('RQ03: Relação entre Atividade e Qualidade de Código\nEvolução das métricas CBO, DIT e LCOM por nível de atividade', fontsize=16, weight='bold', pad=20)
    ax1.set_xlabel('Atividade', fontsize=14)
    ax1.set_ylabel('CBO / DIT', fontsize=14)
    ax2.set_ylabel('LCOM', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['Atividade'], fontsize=13)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax2.grid(False)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=13)
    plt.tight_layout()
    plt.savefig('imagens/rq03_atividade_vs_qualidade.png', dpi=300)
    plt.savefig('imagens/rq03_atividade_vs_qualidade.pdf', dpi=300)
    plt.close()

def main():
    plot_rq01(rq01_df)
    plot_rq03(rq03_df)

if __name__ == '__main__':
    main()
