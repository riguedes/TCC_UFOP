import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Inferify - Indústria",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv(https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Inferify/songs_info.csv)
df_um = pd.read_csv(https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Inferify/artistas_popularidade.csv)
df_dois = pd.read_csv(https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Inferify/artistas_info.csv)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# --- Filtro de Ano (com Slider mais bonito) ---
anos_disponiveis = sorted(df['release_year'].dropna().unique())
ano_min, ano_max = int(min(anos_disponiveis)), int(max(anos_disponiveis))

anos_selecionados = st.sidebar.slider(
    "Intervalo de Anos",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max),
    step=1
)

# --- Filtro de Artista ---
artista_disponiveis = sorted(df['artist'].dropna().unique())
artista_selecionadas = st.sidebar.multiselect(
    "Selecione Artista(s) ou Banda(s)",
    options=artista_disponiveis,
    default=artista_disponiveis[:5],  # mostra só alguns como padrão
    help="Pesquise pelo nome do artista ou banda"
)

# --- Filtro de Álbum ---
album_disponiveis = sorted(df['Album'].dropna().unique())
album_selecionados = st.sidebar.multiselect(
    "Selecione Álbum(s)",
    options=album_disponiveis,
    default=album_disponiveis[:5],
    help="Pesquise pelo nome do álbum"
)

# --- Filtro de Gênero ---
genero = sorted(df['genre'].dropna().astype(str).unique())
genero_um = st.sidebar.multiselect(
    "Selecione Gênero(s) Musicais",
    options=genero,
    default=genero[:5],
    help="Pesquise ou selecione múltiplos gêneros"
)

# --- Filtragem do DataFrame Principal ---
df_filtrado = df[
    (df['release_year'] >= anos_selecionados[0]) &
    (df['release_year'] <= anos_selecionados[1]) &
    (df['artist'].isin(artista_selecionadas)) &
    (df['Album'].isin(album_selecionados)) &
    (df['genre'].isin(genero_um))
]

# --- Conteúdo Principal ---
st.title("Dashboard de Análise do Impacto Musical na Indústria")
st.markdown("Explore os dados musicais desses artistas e bandas em relação ao impacto na Indústria.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas Gerais")

if not df_filtrado.empty:
    qntd_anos = df_filtrado['release_year'].nunique()
    qntd_letras = df_filtrado['lyrics'].nunique()
    qntd_words = df_filtrado['Word Count'].sum()
    qntd_genre = df_filtrado['genre'].nunique()
else:
    qntd_anos, qntd_letras, qntd_words, qntd_genre = 0, 0, 0, 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Anos Analisados", f"{qntd_anos}")
col2.metric("Letras Analisadas", f"{qntd_letras}")
col3.metric("Total de Palavras", f"{qntd_words:,}")
col4.metric("Gêneros Musicais", f"{qntd_genre}")

st.markdown("---")

# 1. Quantidade de músicas lançadas por artista
st.subheader("Quantidade de Músicas por Artista")
musicas_por_artista = df_filtrado.groupby("artist")["title"].count().reset_index().sort_values("title", ascending=False)
fig1 = px.bar(musicas_por_artista, x="artist", y="title", color="title", text="title")
st.plotly_chart(fig1, use_container_width=True)

# 2. Palavras mais frequentes nas letras
st.subheader("Palavras Mais Frequentes nas Letras")
all_lyrics = " ".join(df_filtrado['lyrics'].dropna()).lower()
all_lyrics = re.sub(r'[^a-zA-Z\s]', '', all_lyrics)
words = all_lyrics.split()
word_counts = Counter(words)
most_common_words = pd.DataFrame(word_counts.most_common(20), columns=['word','count'])
fig2 = px.bar(most_common_words, x='word', y='count', color='count', text='count')
st.plotly_chart(fig2, use_container_width=True)

# 3. Total de músicas lançadas por ano
st.subheader("Total de Músicas Lançadas por Ano")
musicas_por_ano = df_filtrado.groupby("release_year")["title"].count().reset_index()
fig3 = px.bar(musicas_por_ano, x="release_year", y="title", color="title", text="title")
st.plotly_chart(fig3, use_container_width=True)

# 4. Distribuição de tamanho das composições
st.subheader("Distribuição de Composições das Músicas")
fig = px.histogram(df_filtrado, x="Word Count", nbins=30)
st.plotly_chart(fig)

# 5. Top Álbuns por Quantidade de Músicas
st.subheader("Top Álbuns com maior Quantidade de Músicas")
top_albuns = df_filtrado.groupby("Album")["title"].count().reset_index().sort_values("title", ascending=False)
fig = px.bar(top_albuns.head(20), x="Album", y="title", color="title", text="title")
st.plotly_chart(fig)

# 6. Evolução das Composições por Ano
media_palavras_ano = df_filtrado.groupby("release_year")["Word Count"].mean().round(0).astype(int).reset_index()
fig = px.line(media_palavras_ano, x="release_year", y="Word Count", markers=True,
              title="Tamanho Médio das Letras por Ano (valores inteiros)")
st.plotly_chart(fig)

# 7. Distribuição de Composições por Artista
st.subheader("Distribuição de Composições por Artista")
fig = px.box(df_filtrado, x="artist", y="Word Count", color="artist")
st.plotly_chart(fig)

# 8. Total de gêneros usados por ano
st.subheader("Total de Gêneros por Ano")
musicas_por_genero = df_filtrado.groupby("release_year")["genre"].nunique().reset_index()
fig8 = px.bar(musicas_por_genero, x="release_year", y="genre", color="genre", text="genre")
st.plotly_chart(fig8, use_container_width=True)

# 9. Top Álbuns por Quantidade de Gêneros
st.subheader("Top Álbuns com maior Quantidade de Gêneros")
top_genre = df_filtrado.groupby("Album")["genre"].nunique().reset_index().sort_values("genre", ascending=False)
fig9 = px.bar(top_genre.head(20), x="Album", y="genre", color="genre", text="genre")

st.plotly_chart(fig9)
