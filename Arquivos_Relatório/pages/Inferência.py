import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Inferify - Inferência de Emoções",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("songs_info.csv")
df_um = pd.read_csv("artistas_popularidade.csv")
df_dois = pd.read_csv("artistas_info.csv")

# --- Colunas que queremos inverter ---
colunas_inverter = ["score","joy","sadness","surprise","trust","anger","disgust","anticipation","fear"]

# --- Inverter sinais ---
for col in colunas_inverter:
    if col in df.columns:
        df[col] = df[col] * -1

# --- Limpeza e padronização ---
df['release_year'] = df['release_year'].astype(int)
df['artist'] = df['artist'].astype(str).str.strip()
df['Album'] = df['Album'].astype(str).str.strip()
df['genre'] = df['genre'].astype(str).str.strip()
df['sentiment'] = df['sentiment'].astype(str).str.strip()

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

anos_disponiveis = sorted(df['release_year'].unique())
anos_selecionados = st.sidebar.multiselect("Ano de Lançamento", anos_disponiveis, default=anos_disponiveis)

artista_disponiveis = sorted(df['artist'].unique())
artista_selecionadas = st.sidebar.multiselect("Artista ou Banda", artista_disponiveis, default=artista_disponiveis)

album_disponiveis = sorted(df['Album'].unique())
album_selecionados = st.sidebar.multiselect("Álbum", album_disponiveis, default=album_disponiveis)

genero = sorted(df['genre'].dropna().unique())
genero_um = st.sidebar.multiselect("Gênero Musical", genero, default=genero)

# --- Filtragem robusta ---
df_filtrado = df[
    df['release_year'].isin(anos_selecionados) &
    df['artist'].isin(artista_selecionadas) &
    df['Album'].isin(album_selecionados) &
    df['genre'].isin(genero_um)
].copy()

# --- Conteúdo Principal ---
st.title("Dashboard de Análise de Emoções")
st.markdown("Explore os dados musicais dessas bandas e artistas em relação à Análise de Sentimentos e Inferência de Emoções.")

# --- Métricas Principais ---
st.subheader("Métricas Gerais")
if not df_filtrado.empty:
    score_medio = df_filtrado['score'].mean()
    score_maximo = df_filtrado['score'].max()
    emocao_mais_frequente = df_filtrado['sentiment'].mode()[0]
    artista_mais_frequente = df_filtrado['artist'].mode()[0]
else:
    score_medio, score_maximo, emocao_mais_frequente, artista_mais_frequente = 0, 0, "", ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Score Médio", f"{score_medio:.2f}")
col2.metric("Score Máximo", f"{score_maximo:.2f}")
col3.metric("Emoção Mais Frequente", emocao_mais_frequente)
col4.metric("Artista Mais Frequente", artista_mais_frequente)

st.markdown("---")

# --- Gráficos ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# Gráfico 1 - Artistas por Score Médio
with col_graf1:
    if not df_filtrado.empty:
        top_artistas = df_filtrado.groupby('artist')['score'].mean().sort_values().reset_index()
        grafico_artistas = px.bar(
            top_artistas,
            x='score',
            y='artist',
            orientation='h',
            title="Artistas por Score Médio",
            labels={'score': 'Score Médio', 'artist': ''}
        )
        grafico_artistas.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_artistas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de artistas.")

# Gráfico 2 - Distribuição de Scores
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='score',
            nbins=30,
            title="Distribuição de Scores",
            labels={'score': 'Score', 'count': 'Quantidade'}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição de scores.")

col_graf3, col_graf4 = st.columns(2)

# Gráfico 3 - Proporção de Sentimentos
with col_graf3:
    if not df_filtrado.empty:
        sentimento_contagem = df_filtrado['sentiment'].value_counts().reset_index()
        sentimento_contagem.columns = ['sentimento', 'quantidade']
        grafico_sentimentos = px.bar(
            sentimento_contagem,
            x='sentimento',
            y='quantidade',
            color='sentimento',
            text='quantidade',
            title='Proporção de Sentimentos nas Músicas'
        )
        grafico_sentimentos.update_layout(title_x=0.1, showlegend=False)
        st.plotly_chart(grafico_sentimentos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de sentimentos.")

# Gráfico 4 - Evolução do Score Médio por Ano
with col_graf4:
    if not df_filtrado.empty:
        score_por_ano = df_filtrado.groupby('release_year')['score'].mean().reset_index()
        grafico_ano = px.line(
            score_por_ano,
            x='release_year',
            y='score',
            title='Evolução do Score Médio por Ano',
            labels={'release_year': 'Ano de Lançamento', 'score': 'Score Médio'}
        )
        grafico_ano.update_layout(title_x=0.1)
        st.plotly_chart(grafico_ano, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico por ano.")

# --- Gráfico 5 - Gêneros por Score Médio ---
if not df_filtrado.empty:
    top_generos = df_filtrado.groupby('genre')['score'].mean().sort_values().reset_index()
    grafico_generos = px.bar(
        top_generos,
        x='score',
        y='genre',
        orientation='h',
        title="Gêneros por Score Médio",
        labels={'score': 'Score Médio', 'genre': ''}
    )
    grafico_generos.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(grafico_generos, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no gráfico de gêneros.")

# --- Gráfico 6 - Heatmap: Distribuição de Gêneros por Sentimento ---
if not df_filtrado.empty:
    genero_contagem_um = df_filtrado.groupby(['sentiment', 'genre']).size().reset_index(name='quantidade')
    
    grafico_heatmap = px.density_heatmap(
        genero_contagem_um,
        x='genre',
        y='sentiment',
        z='quantidade',
        color_continuous_scale='Viridis',
        text_auto=True,
        title='Distribuição de Gêneros por Sentimento'
    )
    
    grafico_heatmap.update_layout(
        xaxis_title="Gênero",
        yaxis_title="Sentimento",
        yaxis={'categoryorder':'total ascending'}
    )
    
    st.plotly_chart(grafico_heatmap, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no heatmap de gêneros por sentimento.")