import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import SimpleRNN
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import speech_recognition as sr
import datetime

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

# ---------------------------
# Fix SimpleRNN load issue
# ---------------------------
def ignore_time_major(**kwargs):
    if 'time_major' in kwargs:
        kwargs.pop('time_major')
    return SimpleRNN(**kwargs)

# ---------------------------
# Load Model
# ---------------------------
word_index = imdb.get_word_index()
model = load_model('simple_rnn_imdb.h5', custom_objects={'SimpleRNN': ignore_time_major})

MAX_WORDS = 10000
DEFAULT_POSTER = "https://via.placeholder.com/300x450?text=No+Image"

# ---------------------------
# CSS for UI
# ---------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h2, h3 { color: white; }
.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
.stTextInput>div>div>input { background-color: #262730; color: white; }
.card { background-color: #1c1c1c; padding: 10px; border-radius: 10px; text-align: center; transition: 0.3s; }
.card:hover { transform: scale(1.05); cursor:pointer; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Helper Functions
# ---------------------------
def preprocess_text(text):
    words = text.lower().split()
    encoded = []
    for word in words:
        index = word_index.get(word, 2) + 3
        if index >= MAX_WORDS:
            index = 2
        encoded.append(index)
    return sequence.pad_sequences([encoded], maxlen=500)

def get_sentiment(pred):
    if pred > 0.7: return "Positive 😊", "green"
    elif pred < 0.3: return "Negative 😞", "red"
    else: return "Neutral 😐", "orange"

def clean_movies(movies):
    return [m for m in movies if m.get("Poster") and m["Poster"] != "N/A"]

def sort_by_year(movies):
    return sorted(movies, key=lambda x: int(x.get("Year", "0")[:4]), reverse=True)

def get_movie_details(name):
    url = f"http://www.omdbapi.com/?t={name}&apikey={API_KEY}"
    res = requests.get(url).json()
    return res if res.get("Response") == "True" else None

def matches_industry(movie, industry):
    country = movie.get("Country", "").lower()
    if not industry or industry.lower()=="all": return True
    if industry.lower()=="hollywood": return "usa" in country
    if industry.lower()=="bollywood": return "india" in country
    return True

def search_movies(query, industry=None, max_results=5):
    url = f"http://www.omdbapi.com/?s={query}&apikey={API_KEY}"
    res = requests.get(url).json()
    if res.get("Response")=="True":
        movies = clean_movies(res.get("Search", []))
        detailed = []
        for m in movies:
            details = get_movie_details(m["Title"])
            if details and matches_industry(details, industry):
                detailed.append(details)
        return sort_by_year(detailed)[:max_results]
    return []

def get_movies_by_genre(genre, industry=None, max_results=12):
    movies=[]
    current_year = datetime.datetime.now().year
    for year in range(current_year, current_year-5, -1):
        url=f"http://www.omdbapi.com/?s={genre}&y={year}&apikey={API_KEY}"
        res = requests.get(url).json()
        if res.get("Response")=="True":
            for m in res.get("Search",[]):
                details = get_movie_details(m["Title"])
                if details and genre.lower() in details.get("Genre","").lower():
                    if matches_industry(details, industry):
                        movies.append(details)
        if len(movies)>=max_results: break
    return movies[:max_results]

def get_recommendations(movie, industry=None, max_results=5):
    genre = movie["Genre"].split(",")[0]
    return get_movies_by_genre(genre, industry=industry, max_results=max_results)

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except:
        st.error("Voice not recognized")
        return ""

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🎬 Netflix AI", layout="wide")
st.markdown("<h1 style='text-align:center; color:#e50914;'>🎬 Movie Analyzer</h1>", unsafe_allow_html=True)

# Genre + Industry
GENRES = ["Action","Comedy","Drama","Horror","Romance","Sci-Fi","Thriller","Adventure","Animation"]
selected_genre = st.selectbox("Choose Genre", GENRES)
INDUSTRIES = ["All","Hollywood","Bollywood","Other"]
selected_industry = st.selectbox("Choose Industry", INDUSTRIES)

# Display genre movies
genre_movies = get_movies_by_genre(selected_genre, selected_industry)
if genre_movies:
    cols = st.columns(6)
    for i,m in enumerate(genre_movies[:6]):
        with cols[i]:
            poster = m.get("Poster") if m.get("Poster") and m["Poster"]!="N/A" else DEFAULT_POSTER
            st.image(poster)
            st.caption(f"{m['Title']} ({m['Year']})")
            if st.button(f"Select", key=f"genre_{i}"):
                st.session_state["selected_movie"] = m["Title"]

# Search with live recommendations
st.markdown("## 🔍 Search Movie")
search_query = st.text_input("Type movie name (min 2 letters)", key="search_input")
selected_movie = st.session_state.get("selected_movie", None)

if search_query and len(search_query) >= 2:
    recs = search_movies(search_query, selected_industry, max_results=5)
    if recs:
        cols = st.columns(len(recs))
        for i, movie in enumerate(recs):
            with cols[i]:
                poster = movie.get("Poster") if movie.get("Poster") and movie["Poster"]!="N/A" else DEFAULT_POSTER
                if st.button("", key=f"rec_{i}"):  # select movie on click
                    selected_movie = movie["Title"]
                    st.session_state["selected_movie"] = selected_movie
                st.image(poster)
                st.markdown(f"**{movie['Title']} ({movie['Year']})**", unsafe_allow_html=True)

# Voice Input
if st.button("🎤 Speak"):
    voice_text = get_voice_input()
    if voice_text:
        search_query = voice_text
        recs = search_movies(search_query, selected_industry, max_results=5)
        if recs:
            cols = st.columns(len(recs))
            for i, movie in enumerate(recs):
                with cols[i]:
                    poster = movie.get("Poster") if movie.get("Poster") and movie["Poster"]!="N/A" else DEFAULT_POSTER
                    if st.button("", key=f"voice_{i}"):
                        selected_movie = movie["Title"]
                        st.session_state["selected_movie"] = selected_movie
                    st.image(poster)
                    st.markdown(f"**{movie['Title']} ({movie['Year']})**", unsafe_allow_html=True)

# Analyze Movie
if st.button("Analyze Movie"):
    if not selected_movie:
        st.warning("Select a movie first")
    else:
        movie = get_movie_details(selected_movie)
        if movie:
            st.markdown("## 🎥 Now Showing")
            col1,col2 = st.columns([1,2])
            with col1:
                poster = movie.get("Poster") if movie.get("Poster") and movie["Poster"]!="N/A" else DEFAULT_POSTER
                st.image(poster)
            with col2:
                st.subheader(movie["Title"])
                st.write("⭐ Rating:", movie.get("imdbRating","N/A"))
                st.write("🎭 Genre:", movie.get("Genre","N/A"))
                st.write("🎬 Actors:", movie.get("Actors","N/A"))
                st.write("🌎 Country:", movie.get("Country","N/A"))
            st.markdown("### 📝 Plot")
            st.write(movie.get("Plot","Plot not available"))
            processed = preprocess_text(movie.get("Plot",""))
            pred = model.predict(processed)[0][0]
            sentiment,color = get_sentiment(pred)
            st.markdown("## 🧠 Sentiment Analysis")
            st.markdown(f"<h3 style='color:{color}'>{sentiment}</h3>", unsafe_allow_html=True)
            st.progress(float(pred))
            st.write("Confidence:", round(pred,4))
            st.markdown("## 🎯 Recommended Movies")
            recs = get_recommendations(movie, selected_industry)
            cols = st.columns(5)
            for i, rec in enumerate(recs[:5]):
                with cols[i]:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    poster = rec.get("Poster") if rec.get("Poster") and rec["Poster"]!="N/A" else DEFAULT_POSTER
                    st.image(poster)
                    st.markdown(f"**{rec['Title']} ({rec['Year']})**")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Movie not found")