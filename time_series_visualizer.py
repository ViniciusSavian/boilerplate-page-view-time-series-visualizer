import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
np.float = float

register_matplotlib_converters()

# Import data (certifique-se de que o caminho para o arquivo está correto)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpar dados
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Desenhar gráfico de linha
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['value'], color='blue', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Salvar imagem e retornar fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar e modificar dados para gráfico de barras mensais
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Desenhar gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 5))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(labels=['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December'], 
              title="Months")

    # Salvar imagem e retornar fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar dados para box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Certificar-se de que a coluna 'value' é numérica
    df_box['value'] = pd.to_numeric(df_box['value'], errors='coerce')

    # Desenhar box plots (usando Seaborn)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Box plot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Box plot por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, 
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Salvar imagem e retornar fig
    fig.savefig('box_plot.png')
    return fig
