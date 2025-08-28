import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Inferify - Página Inicial",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("songs_info.csv")
df_um = pd.read_csv("artistas_popularidade.csv")
df_dois = pd.read_csv("artistas_info.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['release_year'].dropna().unique())
anos_selecionados = st.sidebar.multiselect("Ano de Lançamento", anos_disponiveis, default=anos_disponiveis)

# Filtro de Artista
artista_disponiveis = sorted(df['artist'].dropna().unique())
artista_selecionadas = st.sidebar.multiselect("Artista ou Banda", artista_disponiveis, default=artista_disponiveis)

# Filtro por Álbum
album_disponiveis = sorted(df['Album'].dropna().unique())
album_selecionados = st.sidebar.multiselect("Álbum", album_disponiveis, default=album_disponiveis)

# Filtro por Gênero
genero = sorted(df['genre'].dropna().astype(str).unique())
genero_um = st.sidebar.multiselect("Gênero Musical", genero, default=genero)

# --- Filtragem do DataFrame Principal ---
df_filtrado = df[
    (df['release_year'].isin(anos_selecionados)) &
    (df['artist'].isin(artista_selecionadas)) &
    (df['Album'].isin(album_selecionados)) &
    (df['genre'].isin(genero_um))
]

# --- Aplicar filtros também em df_um e df_dois ---
artistas_filtrados = df_filtrado['artist'].unique()

df_um_filtrado = df_um[df_um['nome'].isin(artistas_filtrados)]

df_dois_filtrado = df_dois[
    (df_dois['nome'].isin(artistas_filtrados)) |
    (df_dois['banda'].isin(artistas_filtrados))
].copy()

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Inferência de Emoções em Músicas")
st.markdown("Explore os dados musicais de letras de bandas e artistas. Utilize os filtros à esquerda caso queira algo específico.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas Gerais")

qntd_artista = df_filtrado['artist'].nunique() if not df_filtrado.empty else 0
total_musicas = df_filtrado.shape[0]
total_albuns = df_filtrado['Album'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Quantidade de Artistas", f"{qntd_artista}")
col2.metric("Total de Músicas", f"{total_musicas:,}")
col3.metric("Total de Álbuns", total_albuns)

st.markdown("---")

# Quantidade de músicas lançadas por gênero musical
st.subheader("Quantidade de Músicas por Gênero")
musicas_por_genero = df_filtrado.groupby("genre")["title"].count().reset_index().sort_values("title", ascending=False)
fig1 = px.bar(musicas_por_genero, x="genre", y="title", color="title", text="title")
st.plotly_chart(fig1, use_container_width=True)

# Quantidade de gêneros musicais usados por artista
st.subheader("Quantidade de Gêneros por Artista")
musicas_por_genero = df_filtrado.groupby("artist")["genre"].nunique().reset_index().sort_values("genre", ascending=False)
fig1 = px.bar(musicas_por_genero, x="artist", y="genre", color="genre", text="genre")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
