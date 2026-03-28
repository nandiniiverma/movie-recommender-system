import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch poster (stable + fallback)
def fetch_poster(movie_id):
    try:
        api_key = "YOUR_API_KEY"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        poster_path = data.get('poster_path')
        
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    
    except:
        pass

    # 🔥 SMART FALLBACK (always works)
    return "https://picsum.photos/300/450"
    # fallback image (always works)
    return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']   # ✅ correct column
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# UI
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.write(names[i])
