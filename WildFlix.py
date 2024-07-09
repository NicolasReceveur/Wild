import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import NearestNeighbors
import urllib.request
import requests
import seaborn as sns
import pydeck as pdk
import altair as alt
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate


#Nos données utilisateurs doivent respecter ce format

lesDonneesDesComptes = {'usernames': {'utilisateur': {'name': 'utilisateur',
   'password': 'utilisateurMDP',
   'email': 'utilisateur@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'utilisateur'},
  'root': {'name': 'root',
   'password': 'rootMDP',
   'email': 'admin@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'administrateur'}}}

authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)

authenticator.login()

df_test= pd.read_csv("df_test.csv")
df_genres = pd.read_csv("df_genres_acp.csv")

if st.session_state["authentication_status"]:
  

#primaryColor="#EF9C82"
#backgroundColor="#123332"
#secondaryBackgroundColor="#1D4241"
#textColor="#FFD9BE"
#font="sans serif"

    with st.sidebar:
        #Le bouton de déconnexion
    
        selection = option_menu(
                    menu_title=None,
                    options = ["WildFlix", "Moteur de recherche", "Projets","Dashboard"],
                    orientation= "vertical"

                )
        authenticator.logout("Déconnexion")

    if selection == "WildFlix":
        #st.set_page_config(
        #   page_title="WILDFIX",
        #)
        #st.title("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(' ')

        with col2:
            st.image('Titre.jpg')

        with col3:
            st.write(' ')

        st.image('WildFlix6h.png')

        st.write(
        '<left><h5>Bienvenue sur le site web de votre cinéma local, où vous découvrirez une riche programmation de films afin de trouver votre prochaine séance idéale. </span></h1></center>',
        unsafe_allow_html=True
        )

        st.write(
        '<left><h5>Depuis son ouverture en 1950, notre cinéma de quartier a traversé les époques, restant un pilier de la communauté. Ses murs gardent les souvenirs de générations de cinéphiles qui ont partagé leur amour du 7e art. </span></h1></center>',
        unsafe_allow_html=True
        )

        st.write(
        '<left><h5>Que vous soyez un cinéphile aguerri ou un amateur de nouvelles découvertes, notre programmation vous réserve des surprises. </span></h1></center>',
        unsafe_allow_html=True
        )


    elif selection == "Moteur de recherche":
        #st.title("")

        st.image('Moteur3.jpg')


        # Titre du tableau de bord
        st.write(
            '<left><h5>Sélectionnez le film de votre choix et laissez-vous guider vers des films similaires </h5></center>',
            unsafe_allow_html=True)
        # Demander si l'utilisateur est mineur de moins de 13 ans
        st.markdown(
            '<p style="font-size:20px; font-weight:bold;">Sélection de films tout public (moins de 13 ans) ?</p>',unsafe_allow_html=True)
        mineur = st.radio("",
                ('Oui', 'Non')
                )

        #mineur = st.radio("Sélection de films tout public (moins de 13 ans) ? ", ('Oui', 'Non'))

        # Filtrer les films en fonction de l'âge
        if mineur == 'Oui':
            df_genres = df_genres[df_genres['movie_title'].isin(df_test[df_test['content_rating'].isin(['G', 'PG'])]['movie_title'])]
        
        # Sélection du film par l'utilisateur
        choix = st.selectbox("", df_genres.movie_title)

        # Initialisation metrics

        #nn = NearestNeighbors(n_neighbors=6, metric="euclidean")
        #nn = NearestNeighbors(n_neighbors=6, metric="cosine")
        #nn = NearestNeighbors(n_neighbors=6, metric="jaccard")
        #nn = NearestNeighbors(n_neighbors=6, metric="minkowski")
        #nn = NearestNeighbors(n_neighbors=6, metric="hamming")
        #nn = NearestNeighbors(n_neighbors=6, metric="haversine")
        #nn = NearestNeighbors(n_neighbors=6, metric="chebyshev")
        nn = NearestNeighbors(n_neighbors=6, metric="manhattan")
        nn.fit(df_genres.drop("movie_title", axis=1).values)

        # Récupérer les caractéristiques du film choisi par l'utilisateur
        ligne = df_genres[df_genres.movie_title == choix].index[0]
        distances, index = nn.kneighbors([df_genres.drop("movie_title", axis=1).iloc[ligne, :]])

        #listeDesRecommandations = df_genres.movie_title[index[0]]
        listeDesRecommandations = df_genres['movie_title'].iloc[index[0]]

        # Clé API pour OMDB
        api_key = "e54b55d6"

        # Fonction pour obtenir les jaquettes de films à l'aide de l'API OMDB
        def get_movie_poster(title):
            url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            return data.get("Poster")

        # Affichage des informations
        st.write("")
        for title in listeDesRecommandations.values[1:]:
            col1, col2, col3 = st.columns([1, 2, 1], gap="large")

            with col1:
                st.write('FILMS')
                st.write('')
                poster_url = get_movie_poster(title)
                if poster_url:
                    st.image(poster_url, caption=title, width=180)
                else:
                    st.write(f"Aucune jaquette trouvée pour {title}")

            with col2:
                st.write('CARACTERISTIQUES')
                df_movies = pd.read_csv("df_test.csv")
                st.write('')
                film_info = df_movies[df_movies['movie_title'] == title].iloc[0]
                st.write(f"<u><b>Titre</b></u>: {film_info['movie_title']}", unsafe_allow_html=True)
                st.write(f"<u><b>Score</b></u>: {film_info['imdb_score']}", unsafe_allow_html=True)
                st.write(f"<u><b>Directeur</b></u>: {film_info['director_name']}", unsafe_allow_html=True)
                st.write(f"<u><b>Acteur</b></u>: {film_info['actor_1_name']}", unsafe_allow_html=True)
                st.write(f"<u><b>Durée</b></u>: {film_info['duration']} minutes", unsafe_allow_html=True)

            with col3:
                st.write(' BANDE ANNONCE ') 
                st.write('')
                imdb_link = df_movies[df_movies['movie_title'] == title]['movie_imdb_link'].values[0]
                st.markdown(f"[Voir sur IMDB]({imdb_link})", unsafe_allow_html=True)

            st.write("---")


    elif selection == "Projets":
        st.write(
        '<center><h2> Projets en cours de développement</span></h1></center>',
        unsafe_allow_html=True
        )
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image('Partage2.jpg')

    elif selection == "Dashboard":
        #st.write('<center><h1> DASHBOARD</span></h1></center>', unsafe_allow_html=True)

        # 1. Nombre de films par genre
        sns.set(style="whitegrid")
        st.header('Nombre de films par genre')
        genres = df_test['genres'].str.split('|').explode()
        films_par_genre = genres.value_counts()
        fig2, ax2 = plt.subplots()
        sns.barplot(y=films_par_genre.index, x=films_par_genre.values, ax=ax2, color="#38807e")
        ax2.set_xlabel('')
        ax2.set_ylabel('')
        for index, value in enumerate(films_par_genre.values):
            ax2.text(value, index, f'{value}', color='black', va="center")
        st.pyplot(fig2)
              
               
        
        # 2. Nombre de films par réalisateur
        sns.set(style="whitegrid")
        st.header('Top 15 des réalisateurs par nombre de films')
        films_par_realisateur = df_test['director_name'].value_counts().head(15)
        fig1, ax1 = plt.subplots()
        #fig1.patch.set_facecolor('white')
        sns.barplot(y=films_par_realisateur.index, x=films_par_realisateur.values, ax=ax1, color="#38807e")
        ax1.set_xlabel('')
        ax1.set_ylabel('')
        for index, value in enumerate(films_par_realisateur.values):
            ax1.text(value, index, f'{value}', color='black', va="center")
        st.pyplot(fig1)

        # 3. 15 films les plus populaires
        st.header('Top 15 des films les plus populaires')
        films_mieux_notes = df_test[['movie_title', 'num_voted_users']].sort_values(by='num_voted_users', ascending=False).head(15)
        fig4, ax4 = plt.subplots()
        sns.barplot(y=films_mieux_notes['movie_title'], x=films_mieux_notes['num_voted_users'], ax=ax4, color="#38807e")
        ax4.set_xlabel('')
        ax4.set_ylabel('')
        ax4.set_xticklabels([f'{int(x/1000)}k' for x in ax4.get_xticks()])
        for index, value in enumerate(films_mieux_notes['num_voted_users']):
            ax4.text(value, index, f'{value}', color='black', va="center")
        st.pyplot(fig4)

        # 4. Films les mieux notés

        sns.set(style="whitegrid")
        st.header('Top des 15 films les mieux notés')
        films_mieux_notes = df_test[['movie_title', 'imdb_score']].sort_values(by='imdb_score', ascending=False).head(15)
        fig4, ax4 = plt.subplots()
        sns.barplot(y=films_mieux_notes['movie_title'], x=films_mieux_notes['imdb_score'], ax=ax4, color="#38807e")
        ax4.set_xlabel('')
        ax4.set_ylabel('')
        for index, value in enumerate(films_mieux_notes['imdb_score']):
            ax4.text(value, index, f'{value:.2f}', color='black', va="center")
        st.pyplot(fig4)

        
elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplis')

   