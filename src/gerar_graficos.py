import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import numpy as np

PASTA = "dados/resultados"
OUT = "graficos_tcc"




# ------------------------------------------------------------
# 6. GERAR GRÁFICOS METODOLOGIA (Boxplot e Heatmap)
# ------------------------------------------------------------

def gerar_graficos_metodologia(caminho_csv='dados/resultados/trilhas_kmeans.csv'):
    df = pd.read_csv(caminho_csv)
    
    # Ordenar as categorias
    cat_order = ['Leve', 'Moderada', 'Pesada', 'Muito Pesada', 'Extrema']
    df['dificuldade'] = pd.Categorical(df['dificuldade'], categories=cat_order, ordered=True)

    # 1. Boxplot: Intensidade Diária por Dificuldade (Figura X)
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='dificuldade', y='intensidade_diaria', palette='viridis', showmeans=True, 
                meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black", "markersize":"5"})
    plt.title('Distribuição da Intensidade Diária por Nível de Dificuldade', fontsize=12, fontweight='bold')
    plt.xlabel('Nível de Dificuldade')
    plt.ylabel('Intensidade Diária')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('graficos_tcc/boxplot_intensidade_dificuldade.png', dpi=300)
    plt.close()

    # 2. Mapa de Calor (Correlação das Variáveis - Figura W)
    plt.figure(figsize=(8, 6))
    colunas_corr = ['distancia_km', 'ganho_elevacao_m', 'inclinacao_media_graus', 
                    'dias_trilha', 'intensidade_diaria', 'indice_concentracao_esforco']
    

    df_corr = df[colunas_corr].rename(columns={
        'distancia_km': 'Distância (km)',
        'ganho_elevacao_m': 'Elevação (m)',
        'inclinacao_media_graus': 'Inclinação (°)',
        'dias_trilha': 'Dias',
        'intensidade_diaria': 'Intensidade Diária',
        'indice_concentracao_esforco': 'Índice Conc. (IC)'
    }).corr()

    mask = np.triu(np.ones_like(df_corr, dtype=bool))
    
    sns.heatmap(df_corr, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", 
                vmin=-1, vmax=1, square=True, linewidths=.5)
    plt.title('Matriz de Correlação das Variáveis', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('graficos_tcc/heatmap_correlacao.png', dpi=300)
    plt.close()
    
    print("Gráficos da Metodologia gerados com sucesso.")


def gerar_graficos_validacao(caminho_dbscan='dados/resultados/trilhas_dbscan.csv'):
    # 1. Gráfico de Barras: Comparação do Silhouette Score (Figura Y)
    # Valores baseados no texto do TCC
    modelos = ['K-Means', 'Hierárquico']
    scores = [0.442, 0.405]

    plt.figure(figsize=(7, 5))
    ax = sns.barplot(x=modelos, y=scores, palette=['#2c7bb6', '#abd9e9'])
    plt.title('Comparação do Índice de Silhouette', fontsize=12, fontweight='bold')
    plt.ylabel('Silhouette Score')
    plt.ylim(0, 0.55)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Adicionando os valores em cima das barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')
        
    plt.tight_layout()
    plt.savefig('graficos_tcc/silhouette_comparacao.png', dpi=300)
    plt.close()

    # 2. Gráfico de Dispersão: Detecção de Outliers com DBSCAN (Figura Z)
    try:
        df_dbscan = pd.read_csv(caminho_dbscan)
        
        # Mapear os clusters para nomes mais claros no gráfico
        df_dbscan['Status'] = df_dbscan['cluster'].apply(
            lambda x: 'Anomalia / Extremo (Ruído)' if x == -1 else 'Padrão (Dentro da Densidade)'
        )
        
        # Definir cores: Vermelho para anomalias, Cinza azulado para normais
        paleta = {'Anomalia / Extremo (Ruído)': '#d73027', 'Padrão (Dentro da Densidade)': '#74add1'}

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_dbscan, x='intensidade_diaria', y='indice_concentracao_esforco', 
                        hue='Status', palette=paleta, s=80, alpha=0.8, edgecolor='black')
        
        plt.title('Identificação de Outliers via DBSCAN', fontsize=12, fontweight='bold')
        plt.xlabel('Intensidade Diária')
        plt.ylabel('Índice de Concentração de Esforço (IC)')
        plt.legend(title='Classificação DBSCAN')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig('graficos_tcc/dbscan_outliers.png', dpi=300)
        plt.close()
        print("Gráficos de Validação (Silhouette e DBSCAN) gerados com sucesso.")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_dbscan} não encontrado. Certifique-se de que o nome está correto.")


def gerar_graficos_discussao_avancados(caminho_csv='dados/resultados/trilhas_kmeans.csv'):
    # Carrega os dados
    df = pd.read_csv(caminho_csv)
    
    # Ordena as categorias logicamente
    cat_order = ['Leve', 'Moderada', 'Pesada', 'Muito Pesada', 'Extrema']
    if 'dificuldade' in df.columns:
        df['dificuldade'] = pd.Categorical(df['dificuldade'], categories=cat_order, ordered=True)

    sns.set_theme(style="whitegrid") # Fundo limpo acadêmico

    # ==========================================
    # FIGURA X: Scatter Plot + KDE (Densidade)
    # Mostra a distribuição e as "zonas" de cada cluster sem confusão visual
    # ==========================================
    plt.figure(figsize=(11, 7))
    
    # 1. Camada de fundo: Manchas de densidade (KDE)
    sns.kdeplot(data=df, x='intensidade_diaria', y='indice_concentracao_esforco', 
                hue='cluster', fill=True, alpha=0.15, palette='viridis', legend=False)
    
    # 2. Camada da frente: Pontos reais (Scatter)
    sns.scatterplot(data=df, x='intensidade_diaria', y='indice_concentracao_esforco', 
                    hue='cluster', palette='viridis', size='dias_trilha', 
                    sizes=(60, 350), alpha=0.9, edgecolor='black', linewidth=0.8)
    
    plt.title('Distribuição Topográfica: Densidade e Concentração de Esforço', fontsize=14, fontweight='bold')
    plt.xlabel('Intensidade Diária (ID)', fontsize=12)
    plt.ylabel('Índice de Concentração de Esforço (IC)', fontsize=12)
    plt.legend(title='Cluster / Dias', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_x_dispersao_kde.png', dpi=300)
    plt.close()

    # ==========================================
    # FIGURA Y: Boxplot + Stripplot
    # Mostra a distribuição estatística + os dados individuais reais
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # 1. Camada de fundo: Boxplot com transparência para não esconder os pontos
    sns.boxplot(data=df, x='dificuldade', y='indice_concentracao_esforco', 
                palette='magma', boxprops=dict(alpha=0.4), showfliers=False)
    
    # 2. Camada da frente: Stripplot (as bolinhas individuais das trilhas)
    sns.stripplot(data=df, x='dificuldade', y='indice_concentracao_esforco', 
                  color='black', alpha=0.7, jitter=True, size=6)
    
    plt.title('Índice de Concentração de Esforço (IC) por Nível de Dificuldade', fontsize=14, fontweight='bold')
    plt.xlabel('Nível de Dificuldade', fontsize=12)
    plt.ylabel('Índice de Concentração de Esforço (IC)', fontsize=12)
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_y_boxplot_stripplot.png', dpi=300)
    plt.close()

    # ==========================================
    # FIGURA Z: Silhouette Modernizado (Barras Horizontais)
    # ==========================================
    modelos = ['K-Means\n(Escolhido)', 'Hierárquico']
    scores = [0.442, 0.405]

    plt.figure(figsize=(7, 4))
    # Barras horizontais são melhores para leitura rápida em apresentações
    ax = sns.barplot(y=modelos, x=scores, palette=['#4daf4a', '#377eb8']) 
    
    # Linha vertical indicando um limite mínimo aceitável estatisticamente
    plt.axvline(x=0.25, color='red', linestyle='--', alpha=0.5, label='Estrutura Aceitável (>0.25)')
    
    plt.title('Comparação de Desempenho: Índice de Silhouette', fontsize=13, fontweight='bold')
    plt.xlabel('Silhouette Score', fontsize=11)
    plt.ylabel('')
    plt.xlim(0, 0.55)
    plt.legend(loc='lower right')
    
    # Anotação dos valores no final da barra
    for p in ax.patches:
        ax.annotate(f'{p.get_width():.3f}', 
                    (p.get_width(), p.get_y() + p.get_height() / 2.), 
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_z_silhouette_horizontal.png', dpi=300)
    plt.close()

    print("Novas Figuras X (KDE), Y (Stripplot) e Z (Horizontal) geradas com sucesso!")
    df = pd.read_csv(caminho_csv)
    
    # Garantir ordenação correta das categorias de dificuldade
    cat_order = ['Leve', 'Moderada', 'Pesada', 'Muito Pesada', 'Extrema']
    if 'dificuldade' in df.columns:
        df['dificuldade'] = pd.Categorical(df['dificuldade'], categories=cat_order, ordered=True)

    # ==========================================
    # Figura X: Dispersão (ID vs IC) com tamanho = dias
    # ==========================================
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='intensidade_diaria', y='indice_concentracao_esforco', 
                    hue='cluster', palette='viridis', size='dias_trilha', sizes=(40, 250), alpha=0.85)
    
    plt.title('Distribuição das Trilhas: Intensidade vs Concentração de Esforço', fontweight='bold')
    plt.xlabel('Intensidade Diária (ID)')
    plt.ylabel('Índice de Concentração de Esforço (IC)')
    plt.legend(title='Cluster / Dias', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_x_dispersao_id_ic.png', dpi=300)
    plt.close()

    # ==========================================
    # Figura Y: Boxplot (IC por Dificuldade)
    # ==========================================
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x='dificuldade', y='indice_concentracao_esforco', palette='magma')
    
    plt.title('Índice de Concentração de Esforço (IC) por Nível de Dificuldade', fontweight='bold')
    plt.xlabel('Nível de Dificuldade')
    plt.ylabel('Índice de Concentração (IC)')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_y_boxplot_ic.png', dpi=300)
    plt.close()

    # ==========================================
    # Figura Z: Comparação do Silhouette
    # ==========================================
    modelos = ['K-Means', 'Hierárquico']
    scores = [0.442, 0.405] # Valores extraídos da sua validação

    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x=modelos, y=scores, palette='coolwarm')
    plt.title('Comparação do Índice de Silhouette', fontweight='bold')
    plt.ylabel('Score')
    plt.ylim(0, 0.55)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')
        
    plt.tight_layout()
    plt.savefig('graficos_tcc/figura_z_silhouette.png', dpi=300)
    plt.close()

    print("Figuras X, Y e Z geradas com sucesso.")
# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
   
    gerar_graficos_metodologia()
    gerar_graficos_validacao()
    gerar_graficos_discussao_avancados()

    print("\n✔ Gráficos gerados")


if __name__ == "__main__":
    main()