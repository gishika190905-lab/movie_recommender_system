import streamlit as st
import pickle
import pandas as pd
import requests
import html
# ===========================PAGE CONFIG================================
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
# =========================CUSTOM CSS===================================
st.markdown(
    """
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
    .section-title {
        color: #d9a7ff;
        font-size: 25px;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 20px;
    }
    .movie-title {
        color: #ffffff;
        font-size: 15px;
        font-weight: 600;
        text-align: center;
        min-height: 45px;
        margin-top: 10px;
    }
    .poster-box {
        background-color: #21182e;
        border: 1px solid #49325e;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .poster-box:hover {
        transform: scale(1.03);
        border-color: #8B5CF6;
        cursor: pointer;
    }
    .details-text {
        color: #d9d1e3;
        font-size: 16px;
        line-height: 1.7;
    }
    .details-label {
        color: #d9a7ff;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ==================LOAD MOVIE DATA===========================
@st.cache_resource
def load_data():
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    with open("movie_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    return similarity, movies
similarity, movies = load_data()
# =====================FETCH MOVIE POSTER====================
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_poster(movie_id):
    try:
        api_key = st.secrets.get("TMDB_API_KEY","")
        if not api_key:
            return None
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
        )
        response = requests.get(
            url,
            params={"api_key": api_key},
            timeout=3
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get(
            "poster_path"
        )
        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500" + poster_path)
    except requests.RequestException:
        return None
    except Exception:
        return None
    return None

# ============# FETCH COMPLETE MOVIE DETAILS===============
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_movie_details(movie_id):
    try:
        api_key = st.secrets.get("TMDB_API_KEY","")
        if not api_key:
            return None
        url = (f"https://api.themoviedb.org/3/movie/{movie_id}")
        response = requests.get(
            url,
            params={ "api_key": api_key,
                "append_to_response": "credits,videos"
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
    except Exception:
        return None
# ================# CLEAR SELECTED MOVIE===================
def clear_selected_movie():
    if "movie_id" in st.query_params:
        del st.query_params["movie_id"]
# ================GET CLICKED MOVIE==================
selected_movie_id = st.query_params.get("movie_id")
selected_movie_details = None
if selected_movie_id:
    try:
        selected_movie_details = fetch_movie_details(
            int(selected_movie_id)
        )
    except (ValueError, TypeError):
        selected_movie_details = None

# ===================RECOMMEND MOVIES===================
def recommend(movie_title):
    movie_index = movies[
        movies["title"] == movie_title
    ].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    recommended_movies = []
    recommended_posters = []
    recommended_ids = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ids.append(movie_id)
    return (recommended_movies,recommended_posters,recommended_ids)
# ======================# PAGE HEADING========================
st.markdown(
    '<h1>🎬 CineMatch</h1>',
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="
        text-align: center;
        color: #c5b8d9;
        font-size: 17px;
        margin-bottom: 30px;
    ">
        Discover movies you'll love based on your choice.
    </div>
    """,
    unsafe_allow_html=True
)
# ====================MOVIE SELECTION========================
st.markdown(
    '<div class="section-title">🍿 Choose a Movie</div>',
    unsafe_allow_html=True
)
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies["title"].values,
    index=None,
    placeholder="Search or select a movie...",
    on_change=clear_selected_movie
)
st.write("")


# =====================RECOMMEND BUTTON====================
if st.button(
    "✨ Recommend Movies",
    use_container_width=True
):
    if selected_movie_name is None:
        st.warning("Please select a movie first.")
    else:
        # Remove old clicked movie details
        clear_selected_movie()
        with st.spinner(
            "Finding movies you'll love..."
        ):
            recommendations, posters, movie_ids = recommend(
                selected_movie_name
            )
        st.session_state.recommendations = (recommendations)
        st.session_state.posters = (posters)
        st.session_state.movie_ids = (movie_ids)
# ================DISPLAY RECOMMENDED MOVIES================
if "recommendations" in st.session_state:
    recommendations = (st.session_state.recommendations)
    posters = (st.session_state.posters)
    movie_ids = (st.session_state.movie_ids)
    st.markdown(
        '<div class="section-title">🎥 Recommended For You</div>',
        unsafe_allow_html=True
    )
    cols = st.columns(5)
    for col, title, poster, movie_id in zip(
        cols,
        recommendations,
        posters,
        movie_ids
    ):
        with col:
            with st.container(
                border=True
            ):
                # -------------CLICKABLE POSTER-------------
                if poster:
                    st.markdown(
                        f"""
<a href="?movie_id={movie_id}" target="_self">
<div class="poster-box">
<img src="{poster}" style="width:100%; border-radius:8px; display:block;">
</div>
</a>
""",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="
                            height: 260px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            background: #30223d;
                            border-radius: 8px;
                            color: #c5b8d9;
                        ">
                            Poster unavailable
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # --------------- MOVIE TITLE-----------
                st.markdown(
                    f"""
                    <div class="movie-title">
                        {html.escape(str(title))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ==========MOVIE DETAILS=================
if selected_movie_details:
    details = selected_movie_details
    movie_title = details.get(
        "title",
        "Movie Details"
    )
    release_date = details.get(
        "release_date",
        "Not available"
    )
    rating = details.get(
        "vote_average",
        0
    )
    overview = details.get(
        "overview",
        "Overview not available."
    )
    # ========  # GET CAST=======
    credits = details.get(
        "credits",
        {}
    )
    cast_list = credits.get(
        "cast",
        []
    )
    cast_names = []
    for actor in cast_list[:8]:
        actor_name = actor.get("name")
        if actor_name:
            cast_names.append(actor_name)
    if cast_names:
        cast_text = ", ".join(cast_names)
    else:
        cast_text = (
            "Cast information not available."
        )


    # ===========# GET TRAILER========
    videos = details.get(
        "videos",
        {}
    )
    video_results = videos.get(
        "results",
        []
    )
    trailer_url = None
    for video in video_results:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):
            trailer_key = video.get(
                "key"
            )
            if trailer_key:
                trailer_url = (
                    "https://www.youtube.com/watch?v="+ trailer_key
                )
                break
    # ==============  # SELECTED MOVIE POSTER======================
    selected_poster = fetch_poster(
        int(selected_movie_id)
    )
    # ===============MOVIE DETAILS HEADING==================
    st.markdown(
        '<div class="section-title">🎬 Movie Details</div>',
        unsafe_allow_html=True
    )
    # =======================DETAILS LAYOUT=========================
    poster_column, details_column = st.columns(
        [1, 2],
        gap="large"
    )
    # ===================LEFT SIDE - POSTER==========================
    with poster_column:
        if selected_poster:
            st.image(
                selected_poster,
                width=300
            )
        else:
            st.markdown(
                """
                <div style="
                    width: 300px;
                    height: 420px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: #30223d;
                    border-radius: 12px;
                    color: #c5b8d9;
                ">
                    Poster unavailable
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========RIGHT SIDE - MOVIE INFORMATION===============
    with details_column:
        with st.container(
            border=True
        ):
            st.markdown(
                f"""
                <div style="
                    color: #ffffff;
                    font-size: 32px;
                    font-weight: 800;
                    margin-bottom: 20px;
                ">
                    {html.escape(str(movie_title))}
                </div>
                """,
                unsafe_allow_html=True
            )
            # -------------------- RELEASE DATE-------------------
            st.markdown(
                f"""
                <div class="details-text">
                    <span class="details-label">
                        📅 Release Date:
                    </span>
                    {html.escape(str(release_date))}
                </div>
                """,
                unsafe_allow_html=True
            )
            # -----------RATING----------
            st.markdown(
                f"""
                <div class="details-text">
                    <span class="details-label">
                        ⭐ Rating:
                    </span>
                    {rating:.1f} / 10
                </div>
                """,
                unsafe_allow_html=True
            )
            # ----------------------OVERVIEW--------------------------
            st.markdown(
                """
                <br>
                <div class="details-label">
                    📝 Overview
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(overview)
            # -------------------CAST-----------------------
            st.markdown(
                """
                <div class="details-label">
                    🎭 Cast
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(cast_text)
            # -------------------- TRAILER------------------------
            if trailer_url:
                st.link_button(
                    "▶ Watch Trailer",
                    trailer_url
                )
            else:
                st.info(
                    "Trailer is not available for this movie."
                )