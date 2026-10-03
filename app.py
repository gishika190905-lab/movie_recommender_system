
import streamlit as st
import pickle
import pandas as pd
import requests
# ------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #100c1c, #21112f, #100c1c);
    color: white;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1 {
    text-align: center;
    color: #ffffff;
    font-size: 44px !important;
    font-weight: 800 !important;
}
.stSelectbox label {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}
.stSelectbox [data-baseweb="select"] {
    background-color: #281b38;
    border-radius: 10px;
}
.stButton > button {
    background: linear-gradient(90deg, #9b4dca, #6c39b5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-size: 17px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #b76be4, #8955d1);
    color: white;
    transform: translateY(-2px);
    border: none;
}
.movie-title {
    color: #ffffff;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    min-height: 45px;
    margin-top: 10px;
}
.section-title {
    color: #d9a7ff;
    font-size: 25px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 20px;
}
.poster-box {
    background-color: #21182e;
    border: 1px solid #49325e;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
# -------------------- LOAD DATA --------------------
@st.cache_resource
def load_data():
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    with open("movie_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    return similarity, movies
similarity, movies = load_data()
# -------------------- FETCH POSTER --------------------
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_poster(movie_id):
    try:
        api_key = st.secrets.get("TMDB_API_KEY", "")
        if not api_key:
            return None
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(
            url,
            params={"api_key": api_key},
            timeout=2
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except requests.RequestException:
        return None
    except Exception:
        return None
    return None
# -------------------- RECOMMEND MOVIES --------------------
def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommended_movies.append(title)
        recommended_posters.append(poster)
    return recommended_movies, recommended_posters
# -------------------- FRONTEND --------------------
st.markdown(
    '<div class="section-title">🍿 Choose a Movie</div>',
    unsafe_allow_html=True
)
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies["title"].values,
    index=None,
    placeholder="Search or select a movie..."
)
st.write("")
if st.button("✨ Recommend Movies", use_container_width=True):
    if selected_movie_name is None:
        st.warning("Please select a movie first.")
    else:
        with st.spinner("Finding movies you'll love..."):
            recommendations, posters = recommend(selected_movie_name)

        st.markdown(
            '<div class="section-title">🎥 Recommended For You</div>',
            unsafe_allow_html=True
        )
        cols = st.columns(5)
        for col, title, poster in zip(cols, recommendations, posters):
            with col:
                with st.container(border=True):
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='height:260px; display:flex;"
                            "align-items:center;justify-content:center;"
                            "background:#30223d;border-radius:8px;"
                            "color:#c5b8d9;'>Poster unavailable</div>",
                            unsafe_allow_html=True
                        )
                    st.markdown(
                        f'<div class="movie-title">{title}</div>',
                        unsafe_allow_html=True
                    )