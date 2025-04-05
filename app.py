import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')  # Using .get() to prevent KeyError
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    # Get top 5 recommended movies (excluding the selected movie)
    for p in distances[1:6]:
        movie_id = movies.iloc[p[0]]['id']

        recommended_movie_names.append(movies.iloc[p[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('🎬 Movie Recommender System')
option = st.selectbox('Choose a Movie', movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(option)

    cols = st.columns(5)  # Display 5 movies in a row
    for col, movie_name, movie_poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(movie_name)
            st.image(movie_poster, use_container_width=True)

