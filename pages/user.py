import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(titles, cosine_sim=cosine_sim, start_index=0, num_recommendations=10):
    indices = []
    for title in titles:
        if title in movies['title'].values:
            indices.append(movies[movies['title'] == title].index[0])
    
    if not indices:
        return []

    sim_scores = sum([cosine_sim[idx] for idx in indices])  # Sum similarities
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Remove input movies from recommendations
    sim_scores = [i for i in sim_scores if i[0] not in indices][start_index:start_index + num_recommendations]

    return movies[['title', 'movie_id']].iloc[[i[0] for i in sim_scores]].reset_index(drop=True)

# Load genres from CSV
user_selected_movies = pd.read_csv('selected_movies.csv')

# Session state to store selected movies and recommendation index
if "emo_recommendations" not in st.session_state:
    st.session_state.emo_recommendations = pd.DataFrame()  # Initialize as an empty DataFrame
if "emo_show_more_button" not in st.session_state:
    st.session_state.emo_show_more_button = False  # Ensure it's hidden initially
if "start_index" not in st.session_state:
    st.session_state.start_index = 0  # Initialize index for pagination

# Ensure Reset on Page Load
if st.session_state.emo_recommendations.empty:
    st.session_state.emo_show_more_button = False  

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

# Streamlit UI
st.title("History")

# Check if selected movies exist in session state
if 'selected_movies' not in st.session_state:
    st.session_state.selected_movies = []  # Initialize if it doesn't exist

# Show selected movies and their posters
if st.session_state.selected_movies:
    num_movies = len(st.session_state.selected_movies)
    selected_cols = st.columns(5)  # Create fixed 5 columns for layout
    start_col = 0
    
    for i, movie in enumerate(st.session_state.selected_movies):
        # Find the corresponding movie data
        movie_data = user_selected_movies[user_selected_movies['title'] == movie].iloc[0]
        movie_id = movie_data['movie_id']
        movie_genre = movie_data['genres']
        
        # Get poster URL from the API
        poster_url = fetch_poster(movie_id)
        
        # Display the movie poster and title in a column
        col = selected_cols[start_col + i]  # Cycle through columns
        with col:
            if poster_url:
                st.image(poster_url, width=130)  # Display poster image
            st.markdown(f"<div align='center'>{movie}</div>", unsafe_allow_html=True)
else:
    st.write("No movie selected.")

st.title("Your Recommendations")
if 'selected_movies' not in st.session_state:
    st.session_state.selected_movies = []  # Initialize if it doesn't exist

# If there are selected movies, fetch recommendations and display
if st.session_state.selected_movies:
    recommendations = get_recommendations(st.session_state.selected_movies)

    # Check if there are recommendations
    if not recommendations.empty:
        # Display in rows of 5 columns
        for i in range(0, len(recommendations), 5):  # Display in rows of 5
            cols = st.columns(5)  # Create 5 columns
            st.write("\n")  # Add space 
            for col, j in zip(cols, range(i, i+5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    poster_url = fetch_poster(movie_id)
                    with col:
                        if poster_url:
                            st.image(poster_url, width=130)  # Display poster image
                        st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True)
else:
    fallback_movies = movies.head(10)
    # Display in rows of 5 columns
    for i in range(0, len(fallback_movies), 5):  # Display in rows of 5
        cols = st.columns(5)  # Create 5 columns
        st.write("\n")  # Add space 
        for col, j in zip(cols, range(i, i+5)):
            if j < len(fallback_movies):
                movie_title = fallback_movies.iloc[j]['title']
                movie_id = fallback_movies.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    if poster_url:
                        st.image(poster_url, width=130)  # Display poster image
                    st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True)