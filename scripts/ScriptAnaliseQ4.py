"""
RQ04: Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

IH04: Repositórios maiores tendem a apresentar piores características 
de qualidade devido à maior complexidade e dificuldade de manutenção.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import seaborn as sns

# Configurar matplotlib
plt.switch_backend('Agg')
plt.style.use('default')
sns.set_palette("husl")

def load_data():
    print("=== RQ04: TAMANHO vs QUALIDADE DE CÓDIGO ===\n")
    print("Carregando dados...")
    
    df = pd.read_csv('ck_summary.csv')
    
    # Converter colunas para numérico
    numeric_cols = ['loc_code', 'loc_comment', 'loc_total',
                   'cbo_avg', 'dit_avg', 'lcom_avg']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Dataset carregado: {len(df)} repositórios")
    return df

def analyze_size_categories(df):
    print("\n=== ANÁLISE POR CATEGORIAS DE TAMANHO ===")
    
    # Definir categorias baseadas em LOC (linhas de código)
    # Usar quartis para criar categorias equilibradas
    loc_quartiles = df['loc_code'].quantile([0.25, 0.5, 0.75]).values
    
    df['size_category'] = pd.cut(df['loc_code'], 
                               bins=[0, loc_quartiles[0], loc_quartiles[1], 
                                    loc_quartiles[2], df['loc_code'].max()], 
                               labels=['Pequeno (Q1)', 'Médio (Q2)', 
                                      'Grande (Q3)', 'Muito Grande (Q4)'],
                               include_lowest=True)
    
    print(f"Categorias baseadas em LOC:")
    print(f"  Pequeno: 0 - {loc_quartiles[0]:,.0f} LOC")
    print(f"  Médio: {loc_quartiles[0]:,.0f} - {loc_quartiles[1]:,.0f} LOC")
    print(f"  Grande: {loc_quartiles[1]:,.0f} - {loc_quartiles[2]:,.0f} LOC")
    print(f"  Muito Grande: {loc_quartiles[2]:,.0f}+ LOC")
    
    # Estatísticas por categoria
    size_metrics = ['loc_code', 'loc_comment']
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
    
    print("\nEstatísticas por categoria de tamanho:")
    for category in df['size_category'].cat.categories:
        cat_data = df[df['size_category'] == category]
        print(f"\n{category} ({len(cat_data)} repositórios):")
        
        # Métricas de tamanho
        print("  Métricas de tamanho:")
        for metric in size_metrics:
            if metric in df.columns:
                valid_data = cat_data[metric].dropna()
                if len(valid_data) > 0:
                    mean_val = valid_data.mean()
                    median_val = valid_data.median()
                    print(f"    {metric}: média={mean_val:,.0f}, mediana={median_val:,.0f}")
        
        # Métricas de qualidade
        print("  Métricas de qualidade:")
        for metric in quality_metrics:
            if metric in df.columns:
                valid_data = cat_data[metric].dropna()
                if len(valid_data) > 0:
                    mean_val = valid_data.mean()
                    std_val = valid_data.std()
                    print(f"    {metric}: {mean_val:.3f} ± {std_val:.3f}")
    
    return df

def correlation_analysis(df):
    print("\n=== ANÁLISE DE CORRELAÇÕES TAMANHO vs QUALIDADE ===")
    
    size_metrics = {
        'loc_code': 'Linhas de Código',
        'loc_comment': 'Linhas de Comentários',
        'loc_total': 'Total de Linhas'
    }
    
    quality_metrics = {
        'cbo_avg': 'CBO (Coupling Between Objects)',
        'dit_avg': 'DIT (Depth of Inheritance Tree)', 
        'lcom_avg': 'LCOM (Lack of Cohesion of Methods)'
    }
    
    correlations = {}
    
    print("Correlações entre métricas de tamanho e qualidade:")
    
    for size_metric, size_desc in size_metrics.items():
        if size_metric not in df.columns:
            continue
            
        print(f"\n--- {size_desc} ---")
        correlations[size_metric] = {}
        
        for quality_metric, quality_desc in quality_metrics.items():
            if quality_metric not in df.columns:
                continue
                
            # Dados válidos
            valid_data = df[[size_metric, quality_metric]].dropna()
            
            if len(valid_data) > 2:
                # Correlação de Pearson
                corr_pearson, p_pearson = pearsonr(valid_data[size_metric], valid_data[quality_metric])
                
                # Correlação de Spearman (mais robusta para outliers)
                corr_spearman, p_spearman = spearmanr(valid_data[size_metric], valid_data[quality_metric])
                
                correlations[size_metric][quality_metric] = {
                    'pearson': corr_pearson,
                    'p_pearson': p_pearson,
                    'spearman': corr_spearman,
                    'p_spearman': p_spearman,
                    'n': len(valid_data)
                }
                
                # Interpretação
                if abs(corr_pearson) < 0.1:
                    strength = "muito fraca"
                elif abs(corr_pearson) < 0.3:
                    strength = "fraca"
                elif abs(corr_pearson) < 0.5:
                    strength = "moderada"
                elif abs(corr_pearson) < 0.7:
                    strength = "forte"
                else:
                    strength = "muito forte"
                
                direction = "positiva" if corr_pearson > 0 else "negativa"
                significance = "significativa" if p_pearson < 0.05 else "não significativa"
                
                print(f"  {quality_desc}:")
                print(f"    Pearson:  r = {corr_pearson:6.4f}, p = {p_pearson:.2e} ({significance})")
                print(f"    Spearman: ρ = {corr_spearman:6.4f}, p = {p_spearman:.2e}")
                print(f"    Força: {strength} {direction}")
                print(f"    N = {len(valid_data)}")
    
    return correlations

def create_correlation_heatmap(correlations):
    print("\n=== GERANDO HEATMAP DE CORRELAÇÕES ===")
    
    # Preparar dados para heatmap
    size_metrics = ['loc_code', 'loc_comment']
    quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
    
    # Matriz de correlações
    corr_matrix = np.zeros((len(size_metrics), len(quality_metrics)))
    p_matrix = np.zeros((len(size_metrics), len(quality_metrics)))
    
    for i, size_metric in enumerate(size_metrics):
        for j, quality_metric in enumerate(quality_metrics):
            if (size_metric in correlations and 
                quality_metric in correlations[size_metric]):
                corr_matrix[i, j] = correlations[size_metric][quality_metric]['pearson']
                p_matrix[i, j] = correlations[size_metric][quality_metric]['p_pearson']
            else:
                corr_matrix[i, j] = np.nan
                p_matrix[i, j] = np.nan
    
    # Criar heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Heatmap com anotações
    im = ax.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    
    # Configurar ticks
    ax.set_xticks(range(len(quality_metrics)))
    ax.set_yticks(range(len(size_metrics)))
    ax.set_xticklabels([m.replace('_avg', '').upper() for m in quality_metrics])
    ax.set_yticklabels([m.replace('_', ' ').title() for m in size_metrics])
    
    # Adicionar valores de correlação
    for i in range(len(size_metrics)):
        for j in range(len(quality_metrics)):
            if not np.isnan(corr_matrix[i, j]):
                # Cor do texto baseada na intensidade
                text_color = 'white' if abs(corr_matrix[i, j]) > 0.5 else 'black'
                significance = '*' if p_matrix[i, j] < 0.05 else ''
                text = f'{corr_matrix[i, j]:.3f}{significance}'
                ax.text(j, i, text, ha="center", va="center", color=text_color, fontweight='bold')
    
    # Configurações do gráfico
    ax.set_title('Correlações entre Tamanho e Qualidade\n(* = p < 0.05)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Métricas de Qualidade', fontsize=12)
    ax.set_ylabel('Métricas de Tamanho', fontsize=12)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlação de Pearson', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig('rq04_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Heatmap salvo: rq04_correlation_heatmap.png")


def main():
    """Função principal"""
    # Carregar dados
    df = load_data()
    
    # Análise por categorias de tamanho
    df = analyze_size_categories(df)
    
    # Análise de correlações
    correlations = correlation_analysis(df)
    
    # Criar visualizações
    create_correlation_heatmap(correlations)
    

if __name__ == "__main__":
    main()