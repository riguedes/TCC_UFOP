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

# --- Aplicar filtros também em df_um e df_dois ---
artistas_filtrados = df_filtrado['artist'].unique()

df_um_filtrado = df_um[df_um['nome'].isin(artistas_filtrados)]

df_dois_filtrado = df_dois[
    (df_dois['nome'].isin(artistas_filtrados)) |
    (df_dois['banda'].isin(artistas_filtrados))
].copy()

# --- Conteúdo Principal ---
st.title("🎲 Inferify - Explorando letras musicais")
st.markdown("O Inferify é um panorama de dados para visualização e análise de dados musicais. Dentre as funcionalidades, é possivel explorar a inferência de emoções a partir das letras das músicas, venha explorar os dados musicais de letras de bandas e artistas. Se quiser algo específico, utilize os filtros à esquerda.")

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

# Quantidade de Álbuns por Artista
st.subheader("Quantidade de Álbuns por Artista")
artist_album = df_filtrado.groupby("artist")["Album"].nunique().reset_index().sort_values("Album", ascending=False)
fig10 = px.bar(artist_album, x="artist", y="Album", color="Album", text="Album")
st.plotly_chart(fig10)

# Quantidade de Álbuns por Ano
st.subheader("Quantidade de Álbuns por Ano")
ano_album = df_filtrado.groupby("release_year")["Album"].nunique().reset_index().sort_values("Album", ascending=False)
fig11 = px.bar(ano_album, x="release_year", y="Album", color="Album", text="Album")
st.plotly_chart(fig11)

st.markdown("---")

# --- Dicionário de Dados ---
st.subheader("📖 Dicionário de Dados")
st.markdown("O dicionário de dados abaixo é para auxiliar no entendimento dos dados apresentado na tabela e auxiliar na compreensão dos gráficos.")
st.markdown("""
| Coluna         | Descrição                                                                 |
|----------------|---------------------------------------------------------------------------|
| **artist**     | Nome do artista ou banda que lançou a música.                             |
| **title**      | Título da música.                                                         |
| **genre**      | Gênero musical da canção.                      |
| **lyrics**     | Letra completa da música.                                                 |
| **Album**      | Nome do álbum ao qual a música pertence.                                  |
| **release_year** | Ano de lançamento da música ou álbum.                                   |
| **Word Count** | Quantidade de palavras presentes na letra da música.                      |
| **score**      | Pontuação atribuída à análise da música.      |
| **sentiment**  | Classificação geral da emoção.          |
| **filter**     | Indicador de intensidade da emoção.                      |
| **joy**        | Intensidade de alegria presente na letra.                                 |
| **sadness**    | Intensidade de tristeza presente na letra.                                |
| **surprise**   | Intensidade de surpresa presente na letra.                                |
| **trust**      | Intensidade de confiança presente na letra.                               |
| **angry**      | Intensidade de raiva presente na letra.                                   |
| **disgust**    | Intensidade de nojo presente na letra.                                    |
| **anticipation** | Intensidade de expectativa/antecipação presente na letra.               |
| **fear**       | Intensidade de medo presente na letra.                                    |
""")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
