import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Inferify - Página Inicial",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Arquivos_Relat%C3%B3rio/songs_info.csv")
df_um = pd.read_csv("https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Arquivos_Relat%C3%B3rio/artistas_popularidade.csv")
df_dois = pd.read_csv("https://raw.githubusercontent.com/riguedes/TCC_UFOP/refs/heads/main/Arquivos_Relat%C3%B3rio/artistas_info.csv")

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
st.title("🎲 Dashboard de Análise de Inferência de Emoções em Músicas")
st.markdown("Explore os dados musicais de letras de bandas e artistas. Utilize os filtros à esquerda caso queira algo específico.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas Gerais")

if not df_dois.empty:
    qntd_banda = df_dois['banda'].nunique()
    qntd_artista = df_dois['nome'].nunique()
    total_musicas = df_filtrado.shape[0]
    total_albuns = df_filtrado['Album'].nunique()
else:
    score_medio, score_maximo, total_musicas, artista_mais_frequente = 0, 0, 0, 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Quantidade de Bandas", f"{qntd_banda}")
col2.metric("Quantidade de Artistas", f"{qntd_artista}")
col3.metric("Total de Músicas", f"{total_musicas:,}")
col4.metric("Total de Álbuns", total_albuns)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# Gráfico 1 - Artistas por Sexo
with col_graf1:
    if not df_dois.empty:
        sexo_contagem = df_dois['sexo'].value_counts().reset_index()
        sexo_contagem.columns = ['sexo', 'quantidade']
        grafico = px.pie(
            sexo_contagem,
            names='sexo',
            values='quantidade',
            title='Quantidade de Artistas por Sexo',
            hole=0.5
        )
        grafico.update_traces(textinfo='percent+label')
        grafico.update_layout(title_x=0.1)
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de sentimentos.")

# Gráfico 2 - Quantidade de Artistas por Banda
with col_graf2:
    if not df_dois.empty:
        # Conta quantos artistas por banda
        contagem = df_dois.groupby("banda")["nome"].nunique().reset_index()
        contagem = contagem.sort_values("nome", ascending=True)  # ordena para facilitar a leitura

        # Gráfico de barras horizontais
        grafico_bar = px.bar(
            contagem,
            x="banda",       # eixo x = quantidade de artistas
            y="nome",         # eixo y = bandas
            orientation="v",   # barras horizontais
            title="Quantidade de Artistas por Banda",
            labels={"banda": "Banda", "nome": "Quantidade de Artistas"}
        )

        grafico_bar.update_layout(title_x=0.1)
        st.plotly_chart(grafico_bar, use_container_width=True)

    else:
        st.warning("Nenhum dado para exibir no gráfico de artistas por banda.")

st.markdown("---")

# Quantidade de músicas lançadas por gênero musical
st.subheader("Quantidade de Músicas por Gênero")
musicas_por_genero = df.groupby("genre")["title"].count().reset_index().sort_values("title", ascending=False)
fig1 = px.bar(musicas_por_genero, x="genre", y="title", color="title", text="title")
st.plotly_chart(fig1, use_container_width=True)

# Quantidade de gêneros musicais usados por artista
st.subheader("Quantidade de Gêneros por Artista")
musicas_por_genero = df.groupby("artist")["genre"].nunique().reset_index().sort_values("genre", ascending=False)
fig1 = px.bar(musicas_por_genero, x="artist", y="genre", color="genre", text="genre")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
