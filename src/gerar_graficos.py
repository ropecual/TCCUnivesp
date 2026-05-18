import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import numpy as np

# ============================================================
# CONFIGURAÇÕES GLOBAIS DE QUALIDADE
# ============================================================

plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 600

plt.rcParams['font.size'] = 13
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 11

sns.set_context("talk")
sns.set_style("whitegrid")

PASTA = "dados/resultados"
OUT = "graficos_tcc"

os.makedirs(OUT, exist_ok=True)

# ============================================================
# GERAR GRÁFICOS METODOLOGIA
# ============================================================

def gerar_graficos_metodologia(caminho_csv='dados/resultados/trilhas_kmeans.csv'):

    df = pd.read_csv(caminho_csv)

    cat_order = [
        'Leve',
        'Moderada',
        'Pesada',
        'Muito Pesada',
        'Extrema'
    ]

    df['dificuldade'] = pd.Categorical(
        df['dificuldade'],
        categories=cat_order,
        ordered=True
    )

    # ========================================================
    # BOXPLOT INTENSIDADE
    # ========================================================

    plt.figure(figsize=(14, 8))

    sns.boxplot(
        data=df,
        x='dificuldade',
        y='intensidade_diaria',
        palette='viridis',
        showmeans=True,
        meanprops={
            "marker": "o",
            "markerfacecolor": "white",
            "markeredgecolor": "black",
            "markersize": "7"
        }
    )

    plt.xlabel('Nível de Dificuldade')
    plt.ylabel('Intensidade Diária')

    plt.grid(
        True,
        linestyle='--',
        alpha=0.6
    )

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/boxplot_intensidade_dificuldade.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    # ========================================================
    # HEATMAP
    # ========================================================

    plt.figure(figsize=(12, 9))

    colunas_corr = [
        'distancia_km',
        'ganho_elevacao_m',
        'inclinacao_media_graus',
        'dias_trilha',
        'intensidade_diaria',
        'indice_concentracao_esforco'
    ]

    df_corr = df[colunas_corr].rename(columns={
        'distancia_km': 'Distância (km)',
        'ganho_elevacao_m': 'Elevação (m)',
        'inclinacao_media_graus': 'Inclinação (°)',
        'dias_trilha': 'Dias',
        'intensidade_diaria': 'Intensidade',
        'indice_concentracao_esforco': 'IC'
    }).corr()

    mask = np.triu(np.ones_like(df_corr, dtype=bool))

    sns.heatmap(
        df_corr,
        mask=mask,
        annot=True,
        cmap='coolwarm',
        fmt=".2f",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=.5
    )

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/heatmap_correlacao.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    print("Gráficos da metodologia gerados.")


# ============================================================
# VALIDAÇÃO
# ============================================================

def gerar_graficos_validacao(
    caminho_dbscan='dados/resultados/trilhas_dbscan.csv'
):

    # ========================================================
    # SILHOUETTE
    # ========================================================

    modelos = ['K-Means', 'Hierárquico']
    scores = [0.442, 0.405]

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(
        x=modelos,
        y=scores,
        palette=['#2c7bb6', '#abd9e9']
    )

    plt.ylabel('Silhouette Score')

    plt.ylim(0, 0.55)

    plt.grid(
        axis='y',
        linestyle='--',
        alpha=0.6
    )

    for p in ax.patches:

        ax.annotate(
            f'{p.get_height():.3f}',
            (
                p.get_x() + p.get_width() / 2.,
                p.get_height()
            ),
            ha='center',
            va='center',
            xytext=(0, 8),
            textcoords='offset points'
        )

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/silhouette_comparacao.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    # ========================================================
    # DBSCAN
    # ========================================================

    try:

        df_dbscan = pd.read_csv(caminho_dbscan)

        df_dbscan['Status'] = df_dbscan['cluster'].apply(
            lambda x: 'Outlier'
            if x == -1
            else 'Padrão'
        )

        paleta = {
            'Outlier': '#d73027',
            'Padrão': '#74add1'
        }

        plt.figure(figsize=(14, 8))

        sns.scatterplot(
            data=df_dbscan,
            x='intensidade_diaria',
            y='indice_concentracao_esforco',
            hue='Status',
            palette=paleta,
            s=120,
            alpha=0.85,
            edgecolor='black',
            linewidth=1.2
        )

        plt.xlabel('Intensidade Diária')
        plt.ylabel('IC')

        plt.legend(title='DBSCAN')

        plt.grid(
            True,
            linestyle='--',
            alpha=0.6
        )

        plt.tight_layout()

        plt.savefig(
            'graficos_tcc/dbscan_outliers.png',
            dpi=600,
            bbox_inches='tight'
        )

        plt.close()

        print("Gráficos de validação gerados.")

    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_dbscan} não encontrado.")


# ============================================================
# DISCUSSÃO
# ============================================================

def gerar_graficos_discussao_avancados(
    caminho_csv='dados/resultados/trilhas_kmeans.csv'
):

    df = pd.read_csv(caminho_csv)

    cat_order = [
        'Leve',
        'Moderada',
        'Pesada',
        'Muito Pesada',
        'Extrema'
    ]

    if 'dificuldade' in df.columns:

        df['dificuldade'] = pd.Categorical(
            df['dificuldade'],
            categories=cat_order,
            ordered=True
        )

    # ========================================================
    # KDE + SCATTER
    # ========================================================

    plt.figure(figsize=(16, 9))

    sns.kdeplot(
        data=df,
        x='intensidade_diaria',
        y='indice_concentracao_esforco',
        hue='cluster',
        fill=True,
        alpha=0.15,
        palette='viridis',
        legend=False
    )

    sns.scatterplot(
        data=df,
        x='intensidade_diaria',
        y='indice_concentracao_esforco',
        hue='cluster',
        palette='viridis',
        size='dias_trilha',
        sizes=(80, 450),
        alpha=0.9,
        edgecolor='black',
        linewidth=1
    )

    plt.xlabel('Intensidade Diária (ID)')
    plt.ylabel('IC')

    plt.legend(
        title='Cluster / Dias',
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/figura_x_dispersao_kde.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    # ========================================================
    # BOXPLOT + STRIPPLOT
    # ========================================================

    plt.figure(figsize=(14, 8))

    sns.boxplot(
        data=df,
        x='dificuldade',
        y='indice_concentracao_esforco',
        palette='magma',
        boxprops=dict(alpha=0.4),
        showfliers=False
    )

    sns.stripplot(
        data=df,
        x='dificuldade',
        y='indice_concentracao_esforco',
        color='black',
        alpha=0.7,
        jitter=True,
        size=8
    )

    plt.xlabel('Nível de Dificuldade')
    plt.ylabel('IC')

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/figura_y_boxplot_stripplot.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    # ========================================================
    # SILHOUETTE HORIZONTAL
    # ========================================================

    modelos = ['K-Means\n(Escolhido)', 'Hierárquico']
    scores = [0.442, 0.405]

    plt.figure(figsize=(10, 5))

    ax = sns.barplot(
        y=modelos,
        x=scores,
        palette=['#4daf4a', '#377eb8']
    )

    plt.axvline(
        x=0.25,
        color='red',
        linestyle='--',
        alpha=0.5,
        label='> 0.25'
    )

    plt.xlabel('Silhouette Score')

    plt.ylabel('')

    plt.xlim(0, 0.55)

    plt.legend(loc='lower right')

    for p in ax.patches:

        ax.annotate(
            f'{p.get_width():.3f}',
            (
                p.get_width(),
                p.get_y() + p.get_height() / 2.
            ),
            ha='left',
            va='center',
            xytext=(5, 0),
            textcoords='offset points',
            fontweight='bold'
        )

    plt.tight_layout()

    plt.savefig(
        'graficos_tcc/figura_z_silhouette_horizontal.png',
        dpi=600,
        bbox_inches='tight'
    )

    plt.close()

    print("Figuras da discussão geradas.")


# ============================================================
# GRÁFICO 3D
# ============================================================

def gerar_grafico_3d_kmeans(
    caminho_csv='dados/resultados/trilhas_kmeans.csv'
):

    from mpl_toolkits.mplot3d import Axes3D

    df = pd.read_csv(caminho_csv)

    cat_order = [
        'Leve',
        'Moderada',
        'Pesada',
        'Muito Pesada',
        'Extrema'
    ]

    if 'dificuldade' in df.columns:

        df['dificuldade'] = pd.Categorical(
            df['dificuldade'],
            categories=cat_order,
            ordered=True
        )

    color_map = {
        'Leve': '#2ca02c',
        'Moderada': '#1f77b4',
        'Pesada': '#ff7f00',
        'Muito Pesada': '#d62728',
        'Extrema': '#9467bd'
    }

    fig = plt.figure(figsize=(18, 13))

    ax = fig.add_subplot(
        111,
        projection='3d'
    )

    for cat in cat_order:

        subset = df[df['dificuldade'] == cat]

        color = color_map[cat]


        ax.scatter(
            subset['intensidade_diaria'],
            subset['indice_concentracao_esforco'],
            subset['dias_trilha'],
            s=180,
            label=cat,
            alpha=0.95,
            edgecolors='black',
            linewidths=1.5,
            color=color
        )

        for _, row in subset.iterrows():

            ax.plot(
                [row['intensidade_diaria'],
                 row['intensidade_diaria']],

                [row['indice_concentracao_esforco'],
                 row['indice_concentracao_esforco']],

                [0, row['dias_trilha']],

                linestyle='--',
                alpha=0.45,
                color=color,
                linewidth=2
            )


    ax.set_xlabel(
        'Intensidade Diária (ID)',
        fontsize=15,
        labelpad=18
    )

    ax.set_ylabel(
        'Índice de Conc. de Esforço (IC)',
        fontsize=15,
        labelpad=18
    )

    ax.set_zlabel(
        'Dias de Trilha',
        fontsize=15,
        labelpad=12
    )

    ax.set_zlim(bottom=0)


    ax.view_init(
        elev=28,
        azim=130
    )


    plt.legend(
        title='Dificuldade',
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=12,
        title_fontsize=13,
        frameon=True
    )

    plt.tight_layout()



    plt.savefig(
        'graficos_tcc/kmeans_3d_ultra_hd.png',
        dpi=800,
        bbox_inches='tight'
    )

    plt.close()

# ============================================================
# MAIN
# ============================================================

def main():

    gerar_graficos_metodologia()

    gerar_graficos_validacao()

    gerar_graficos_discussao_avancados()

    gerar_grafico_3d_kmeans()


if __name__ == "__main__":
    main()