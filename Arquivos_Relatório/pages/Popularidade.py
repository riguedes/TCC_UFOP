import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Inferify - Popularidade",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("songs_info.csv")
df_um = pd.read_csv("artistas_popularidade.csv")
df_dois = pd.read_csv("artistas_info.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['release_year'].unique())
anos_selecionados = st.sidebar.multiselect("Ano de Lançamento", anos_disponiveis, default=anos_disponiveis)

# Filtro de Artista
artista_disponiveis = sorted(df['artist'].unique())
artista_selecionadas = st.sidebar.multiselect("Artista ou Banda", artista_disponiveis, default=artista_disponiveis)

# Filtro por Álbum
album_disponiveis = sorted(df['Album'].unique())
album_selecionados = st.sidebar.multiselect("Álbum", album_disponiveis, default=album_disponiveis)

# Filtro por Gênero
genero = sorted(df['genre'].dropna().astype(str).unique())
genero_um = st.sidebar.multiselect("Gênero Musical", genero, default=genero)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['release_year'].isin(anos_selecionados)) &
    (df['artist'].isin(artista_selecionadas)) &
    (df['Album'].isin(album_selecionados)) &
    (df['genre'].isin(genero_um))
]

# --- Conteúdo Principal ---
st.title(" Dashboard de Análise de Popularidade no Spotify")
st.markdown("Explore os dados musicais de popularidade de bandas e artistas oriundos do reality show The X Factor com base na coleta de dados na API do Spotify.")

st.markdown("---")

# 1. Top 10 artistas por popularidade
st.subheader("Top 10 Artistas por Popularidade")
top_pop = df_um.sort_values("popularidade", ascending=False).head(10)
fig1 = px.bar(top_pop, x="nome", y="popularidade", color="popularidade", text="popularidade")
st.plotly_chart(fig1, use_container_width=True)

# 2. Top 10 artistas por seguidores
st.subheader("Top 10 Artistas por Seguidores")
top_seg = df_um.sort_values("seguidores", ascending=False).head(10)
fig2 = px.bar(top_seg, x="nome", y="seguidores", color="seguidores", text="seguidores")
st.plotly_chart(fig2, use_container_width=True)

# 3. Dispersão Popularidade x Seguidores
st.subheader("Popularidade vs Seguidores")
fig3 = px.scatter(df_um, x="seguidores", y="popularidade", size="popularidade", 
                  color="tipo", hover_name="nome", log_x=True)
st.plotly_chart(fig3, use_container_width=True)

# 4. Distribuição da popularidade por tipo
st.subheader("Distribuição da Popularidade por Tipo")
fig4 = alt.Chart(df_um).mark_boxplot().encode(
    x="tipo",
    y="popularidade",
    color="tipo"
)
st.altair_chart(fig4, use_container_width=True)

# 5. Artistas mais populares com imagem
st.subheader("Ranking Geral de Popularidade")
# Ordenar do maior para o menor
df_sorted = df_um.sort_values("popularidade", ascending=False)
cols = st.columns(5)
for i, row in enumerate(df_sorted.itertuples()):
    with cols[i % 5]:
        st.image(row.imagem_principal, caption=f"{row.nome} ({row.popularidade})")

# 6. Média de popularidade por tipo
st.subheader("Média de Popularidade por Tipo de Artista")

mean_pop = df_um.groupby("tipo")["popularidade"].mean().round(0).astype(int).reset_index()

fig6 = px.bar(mean_pop, 
              x="tipo", 
              y="popularidade", 
              color="tipo", 
              text="popularidade")

st.plotly_chart(fig6, use_container_width=True)