import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------- Load data ----------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- TMDB Poster Function ----------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fa050330b51a9b0ac50c35252ff0183e&language=en-US"
        response = requests.get(url)

        if response.status_code != 200:
            return "https://via.placeholder.com/300x450?text=No+Image"

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=No+Image"


# ---------------- Recommendation Function ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------------- UI ----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0b0b0b;
    color: white;
}

h1 {
    color: #e50914;
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

.stSelectbox > div > div {
    background-color: #222;
    color: white;
}

.stButton > button {
    background-color: #e50914;
    color: white;
    border: none;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #b00610;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 NETFLIX STYLE MOVIE RECOMMENDER")

selected_movie_name = st.selectbox(
    "Search or choose a movie",
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    st.subheader("Top 5 Recommendations")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)