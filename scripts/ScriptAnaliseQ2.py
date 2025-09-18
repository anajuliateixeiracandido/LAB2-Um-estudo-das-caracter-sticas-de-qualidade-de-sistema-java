"""
RQ02: Qual a relação entre a maturidade dos repositórios e suas características de qualidade?

IH02: Repositórios mais maduros tendem a apresentar qualidade superior
com menor acoplamento (CBO) e menor profundidade de herança (DIT).
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
    print("=== RQ02: MATURIDADE vs QUALIDADE DE CÓDIGO ===\n")
    print("Carregando dados...")
    
    df = pd.read_csv('ck_summary.csv')
    
    # Converter colunas para numérico
    numeric_cols = ['age_years', 'cbo_avg', 'dit_avg']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Dataset carregado: {len(df)} repositórios")
    return df

def analyze_maturity_categories(df):
    print("\n=== ANÁLISE POR CATEGORIAS DE MATURIDADE ===")
    
    # Definir categorias de maturidade baseadas na idade
    df['maturity_category'] = pd.cut(df['age_years'], 
                                   bins=[0, 3, 7, 12, 20], 
                                   labels=['Jovem (0-3 anos)', 'Médio (3-7 anos)', 
                                          'Maduro (7-12 anos)', 'Muito Maduro (12+ anos)'],
                                   include_lowest=True)
    
    # Estatísticas por categoria
    quality_metrics = ['cbo_avg', 'dit_avg']
    
    print("Estatísticas por categoria de maturidade:")
    for category in df['maturity_category'].cat.categories:
        cat_data = df[df['maturity_category'] == category]
        print(f"\n{category} ({len(cat_data)} repositórios):")
        
        for metric in quality_metrics:
            if metric in df.columns:
                valid_data = cat_data[metric].dropna()
                if len(valid_data) > 0:
                    mean_val = valid_data.mean()
                    std_val = valid_data.std()
                    print(f"  {metric}: {mean_val:.3f} ± {std_val:.3f}")
    
    return df

def correlation_analysis(df):
    print("\n=== ANÁLISE DE CORRELAÇÕES ===")
    
    quality_metrics = {
        'cbo_avg': 'CBO (Coupling Between Objects)',
        'dit_avg': 'DIT (Depth of Inheritance Tree)'
    }
    
    correlations = {}
    
    for metric, description in quality_metrics.items():
        if metric in df.columns:
            # Dados válidos
            valid_data = df[['age_years', metric]].dropna()
            
            if len(valid_data) > 2:
                # Correlação de Pearson
                corr_pearson, p_pearson = pearsonr(valid_data['age_years'], valid_data[metric])
                
                # Correlação de Spearman (não-paramétrica)
                corr_spearman, p_spearman = spearmanr(valid_data['age_years'], valid_data[metric])
                
                correlations[metric] = {
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
                
                print(f"\n{description}:")
                print(f"  Pearson:  r = {corr_pearson:6.4f}, p = {p_pearson:.2e} ({significance})")
                print(f"  Spearman: ρ = {corr_spearman:6.4f}, p = {p_spearman:.2e}")
                print(f"  Força: {strength} {direction}")
                print(f"  Observações: {len(valid_data)}")
    
    return correlations

def create_comprehensive_plots(df):
    print("\n=== GERANDO GRÁFICOS ===")
    
    quality_metrics = {
        'cbo_avg': 'CBO (Coupling Between Objects)',
        'dit_avg': 'DIT (Depth of Inheritance Tree)'
    }
    
    # Gráfico de correlação múltipla
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    for i, (metric, description) in enumerate(quality_metrics.items()):
        if metric in df.columns and i < 4:
            valid_data = df[['age_years', metric]].dropna()
            
            if len(valid_data) > 0:
                # Scatter plot
                axes[i].scatter(valid_data['age_years'], valid_data[metric], 
                              alpha=0.6, s=30)
                
                # Linha de tendência
                z = np.polyfit(valid_data['age_years'], valid_data[metric], 1)
                p = np.poly1d(z)
                axes[i].plot(valid_data['age_years'], p(valid_data['age_years']), 
                           "r--", alpha=0.8, linewidth=2)
                
                # Correlação
                corr, p_val = pearsonr(valid_data['age_years'], valid_data[metric])
                
                axes[i].set_xlabel('Idade do Repositório (anos)')
                axes[i].set_ylabel(description)
                axes[i].set_title(f'{description}\nr = {corr:.3f}, p = {p_val:.2e}')
                axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('rq02_maturity_vs_quality_comprehensive.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Gráfico salvo: rq02_maturity_vs_quality_comprehensive.png")
    
    
def main():
    """Função principal"""
    # Carregar dados
    df = load_data()
    
    # Análise por categorias de maturidade
    df = analyze_maturity_categories(df)
    
    # Análise de correlações
    correlations = correlation_analysis(df)
    
    # Criar gráficos
    create_comprehensive_plots(df)
    

if __name__ == "__main__":
    main()
