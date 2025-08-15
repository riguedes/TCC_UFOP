# Trabalho de Conclusão de Curso
Trabalho de Conclusão de Curso (TCC) pela Universidade Federal de Ouro Preto com o tema: Inferindo Emoções em Músicas Através do Processamento de Linguagem Natural e Metadados Musicais. Este repositório irá conter o projeto prático que tem como objetivo inferir emoções em músicas a partir de análise de letras e extração de metadados usando API's públicas de músicas. O estudo utiliza Processamento de Linguagem Natural (PLN) e técnicas de análise de dados para Recuperação de Informação Musical.

O resultado final está disponível em: https://inferify.streamlit.app/

## 📌Problema de Pesquisa
Os dados e metadados desempenham um papel crucial na indústria musical ao impulsionar a consolidação de artistas em um mercado altamente competitivo. No ramo do áudio digital especificamente, notamos que serviços que se destacam no mercado, como o Spotify ou Last.fm por exemplo, não se limitam somente ao seu catálogo, mas também oferecem uma gama de serviços de análise dos metadados das músicas.

O problema de pesquisa consiste em investigar como algoritmos de IA, especialmente os de PLN, podem ser aplicados no contexto da RIM para explorar e compreender as emoções contidas nas músicas. Assim, busca-se identificar como esses insights podem ser utilizados para revelar pontos de fricção e oportunidades na estratégia da indústria musical, além de mensurar o impacto emocional, contribuindo para o desenvolvimento de abordagens mais eficazes no setor.

Plataformas de streaming de música, como Deezer e Spotify, estão cada vez mais inseridas no cotidiano das pessoas, seja em ambiente de trabalho ou lazer. As músicas podem gerar respostas emocionais em ouvintes, que muitas vezes são desconhecidas ou não intencionais. Aplicar métodos de PLN e de RIM para inferir as emoções “contidas” nas músicas poderia gerar valiosas informações tanto para usuários quanto para a indústria musical.

Dessa forma, o problema pode ser solucionado na questão de analisar esses dados por meio de algoritmos que exploram a questão de sentimentalismo humano, bem como a possibilidade de conseguir gráficos intuitivos e interativos de fácil compreensão a qualquer perfil de usuário.

## 📌Questões Norteadoras
1. Como algoritmos de PLN e extração de metadados musicais podem ser aplicados para identificar emoções nas músicas?
2. De que forma podemos analisar e quantificar os dados e metadados de API's públicas de Recuperação de Informação Musical?
3. Quais pontos de fricção e oportunidades podem ser identificados a partir dos insights emocionais extraídos das músicas?

## 📌Objetivos
O objetivo geral do trabalho consiste em aplicar técnicas de PLN e de RIM para inferir emoções expressas em obras musicais. Nesse contexto, os objetivos específicos são:

1. Identificar métodos de PLN e RIM para inferência de emoções;
2. Coletar dados e metadados de obras musicais a serem utilizadas no estudo de caso;
3. Aplicar métodos de PLN para inferir emoções a partir das letras das músicas;
4. Aplicar métodos de RIM para inferir emoções a partir de metadados musicais;
5. Montar um panorama interativo para apresentação dos resultados.

## 📌Tecnologias Utilizadas
1. Python (Linguagem principal)
2. Jupyter (Ambiente de Programação)
3. NLTK (Para Processamento de Linguagem Natural)
4. API do Spotify (Para extração de features acústicas)
5. Pandas, NumPy (Para manipulação de dados)
6. Matplotlib, Seaborn (Para visualização de resultados)
7. API Genius (Para extração de letras musicais)
8. Arquivo NRC (Para usar a biblioteca NLTK)
9. Scipy (Para normalizar dados)
10. Shapely e Descartes (Para cálculos geométricos)
11. Wordcloud (Para gerar nuvem de palavras)
12. SQLite 3 (para gerar banco de dados)
13. Os, Requests e Re (para manipular requisições de API na web)

## 📌Contexto
Analisar a evolução emocional e lírica de artistas que seguiram carreira solo após a dissolução (disband) de bandas formadas em realities musicais, com foco especial em grupos oriundos do programa The X Factor. A investigação será centrada nas três bandas mais proeminentes reveladas pelo programa: Fifth Harmony, Little Mix e One Direction. A partir de uma abordagem analítica sobre letras de músicas e elementos de identidade artística, busca-se compreender como os ex-integrantes se reposicionaram no cenário musical como artistas solos.

O estudo irá explorar se esses artistas mantiveram as estratégias líricas e emocionais utilizadas durante o período em que faziam parte das bandas, ou se optaram por uma reinvenção estética e identitária. Pretende-se observar, ainda, se o sucesso individual foi construído com base em estratégias autorais próprias, com auxílio de diretrizes da indústria musical, ou mesmo como uma ruptura intencional com a imagem consolidada pela banda.

Ao analisar essas trajetórias, o projeto pretende identificar padrões de continuidade ou ruptura nas narrativas musicais, no branding artístico e na forma como esses músicos lidam com as expectativas deixadas pelo sucesso coletivo anterior. A pesquisa espera contribuir para a compreensão de como artistas oriundos de formações coletivas se adaptam ao mercado solo, especialmente sob a ótica da construção emocional e estratégica de suas carreiras musicais.

## 📌Arquivos gerados

- `songs_info.csv`: dados tratados e normalizados resultantes dos notebooks construídos;
- `Artista.db`: Banco de Dados SQL com os dados resultantes da API LyricGenius;
- `ArtistaLyrics.csv`: arquivo CSV com os dados tratados da API LyricGenius;
- `Lyric_Artista.json`: arquivo JSON resultante da requisição da API LyricGenius;
- `NRC.tsv`: arquivo para análise de sentimentos;
- `artistas_info.csv`: dados categóricos dos artistas e bandas;
- `artista_popularidade.csv`: metadados coletados da API Spotify

## 📌Como utilizar

Para executar os notebooks, é necessário um ambiente com *Python3* e dependências que podem ser instaladas via [Pip](https://pypi.org/project/pip/):

Coleta das letras de músicas usando a API LyricGenius

```python
!pip install pandas
!pip install lyricgenius
!pip install nltk
```

Acesso à API do Spotify:

```python
!pip install pandas
!pip install spotipy
```
