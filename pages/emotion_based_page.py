import streamlit as st
import pandas as pd
import numpy as np
import requests
import tensorflow as tf
import pickle

# Load the processed data and similarity matrix
with open('movie_emotion.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Load the trained LSTM model
lstm_model = tf.keras.models.load_model("lstm_movie_model.h5")

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

# Emotion-to-Genre Mapping
if "emotion_genre_map" not in st.session_state:
    st.session_state.emotion_genre_map = {
        'Curious': ['mystery', 'documentary'],
        'Excited': ['adventure', 'fantasy', 'action', 'science fiction'],
        'Happy': ['adventure', 'animation'],
        'Hopeful': ['science fiction', 'biography'],
        'Inspirational': ['biography', 'war', 'history'],
        'Loving': ['romance', 'teen'],
        'Relieved': ['comedy', 'family'],
        'Surprised': ['mystery', 'fantasy', 'thriller', 'adventure'],
        'Angry': ['action', 'thriller'],
        'Bored': ['crime', 'tv movie', 'slice of life'],
        'Confused': ['mystery', 'psychological'],
        'Sad': ['drama', 'horror'],
        'Fearful': ['adventure', 'animation', 'comedy'],
        'Frustrated': ['crime', 'thriller'],
        'Lonely': ['foreign', 'drama', 'family'],
        'Nostalgic': ['history', 'war'],
        'Tense': ['thriller', 'mystery']
    }

# Function to Get Movie Recommendations Using LSTM
def get_recommendations(emotion, start_index=0, num_results=10):
    if emotion not in st.session_state.emotion_genre_map:
        return pd.DataFrame()
    
    genre = st.session_state.emotion_genre_map[emotion]
    filtered_movies = movies[movies['genres'].apply(lambda x: any(g in x for g in genre))]

    if filtered_movies.empty:
        return pd.DataFrame()
    
    # Extract Features (Example: Popularity, Vote_Average, Vote_Count)
    features = filtered_movies[['popularity', 'vote_average', 'vote_count']].values
    features = np.expand_dims(features, axis=1)  # Reshape for LSTM model

    # Predict Scores using LSTM Model
    scores = lstm_model.predict(features)

    # Add scores and sort by highest recommendation
    filtered_movies = filtered_movies.assign(score=scores.flatten())
    ranked_movies = filtered_movies.sort_values(by='score', ascending=False).iloc[start_index:start_index + num_results]

    return ranked_movies[['title', 'id', 'genres', 'score']]

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

st.markdown("""
    <h1 style='text-align: left; font-size:44px; font-weight:bold;'>
        Emotion-Based<br>Movie Recommendation System
    </h1>
""", unsafe_allow_html=True)

# Emotion selection dropdown
emotion = st.selectbox(
    "Select an emotion:",
    ['Curious', 'Excited', 'Happy', 'Hopeful', 'Inspirational',  
    'Loving', 'Relieved', 'Surprised', 'Angry', 'Bored', 'Confused', 
    'Sad', 'Fearful', 'Frustrated', 'Lonely', 'Nostalgic', 'Tense'], index=None
)

col1, col2 = st.columns([0.24, 0.05])  # Adjust column width as needed

with col2:
    emo_recommendations_clicked = st.button("Recommend")

if emo_recommendations_clicked:
    if not emotion:
        st.warning("Please select any emotion.")
    else:
        st.session_state.start_index = 0  # Reset index for fresh recommendations
        st.session_state.emo_recommendations = get_recommendations(emotion)
        
        if st.session_state.emo_recommendations.empty:
            st.error("No recommendations found for this emotion.")
        else:
            st.session_state.emo_show_more_button = True  # Enable "More Recommendations" button
            st.subheader("Top 10 Recommended Movies:")
            
            for i in range(0, len(st.session_state.emo_recommendations), 5):  # Display in rows of 5
                cols = st.columns(5)
                st.write("\n")  # Add space 
                for col, j in zip(cols, range(i, i+5)):
                    if j < len(st.session_state.emo_recommendations):
                        movie_title = st.session_state.emo_recommendations.iloc[j]['title']
                        movie_id = st.session_state.emo_recommendations.iloc[j]['id']
                        poster_url = fetch_poster(movie_id)
                        with col:
                            if poster_url:
                                st.image(poster_url, width=130)
                            st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True)

# Re-Recommendation Button
if "emo_show_more_button" in st.session_state and st.session_state.emo_show_more_button:
    with col1:
        re_emo_recommendations_clicked = st.button("Get More Recommendations")

    if re_emo_recommendations_clicked:
        if "emo_show_more_button" in st.session_state and st.session_state.emo_show_more_button:
                st.session_state.start_index += 10  # Fetch next set of movies
                more_recommendations = get_recommendations(emotion, st.session_state.start_index)
                
                if more_recommendations.empty:
                    st.warning("No more recommendations available.")
                else:
                    st.session_state.emo_recommendations = pd.concat([st.session_state.emo_recommendations, more_recommendations])
                    for i in range(st.session_state.start_index, len(st.session_state.emo_recommendations), 5):
                        cols = st.columns(5)
                        st.write("\n")  # Add space 
                        for col, j in zip(cols, range(i, i+5)):
                            if j < len(st.session_state.emo_recommendations):
                                movie_title = st.session_state.emo_recommendations.iloc[j]['title']
                                movie_id = st.session_state.emo_recommendations.iloc[j]['id']
                                poster_url = fetch_poster(movie_id)
                                with col:
                                    if poster_url:
                                        st.image(poster_url, width=130)
                                    st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True) 

# Customizing Emotion-to-Genre Mapping

st.write("\n")  # Add space 
st.subheader("Customize genres to match your mood")

st.write("\n")  # Add space 
# Emotion to edit
emotion_to_edit = st.selectbox("Select an emotion to edit:", list(st.session_state.emotion_genre_map.keys()), index=None)

if emotion_to_edit:
    st.divider()

    # Display all available genres in the dataset
    all_genres = list(set([genre for sublist in movies['genres'] for genre in sublist if genre not in ['music', 'tv movie']]))
    st.write(f"**Available Genres:**")
    st.caption(" / ".join(sorted(all_genres)))
    
    st.write(f"Current genres for ***{emotion_to_edit}***: {', '.join(st.session_state.emotion_genre_map[emotion_to_edit])}")
    
    new_genres = st.text_area("Enter new genres (comma separated):", value=", ".join(st.session_state.emotion_genre_map[emotion_to_edit]))

    # Column Layout for the "Update Genres" button
    col1, col2 = st.columns([4, 0.927])  # Adjust the column widths as needed

    with col2:
        # Add the 'update-genres-btn' class to this button
        st.markdown(
            """
            <style>
                .update-genres-btn .stButton>button {
                    display: flex;
                    justify-content: flex-end;
                }
            </style>
            """, unsafe_allow_html=True)
        # Add the button with a custom class for right alignment
        update_button = st.button("Update Genres", key="update_genres", help="Update genres for this emotion")

    if update_button:
        updated_genres = [genre.strip() for genre in new_genres.split(',')]
        st.session_state.emotion_genre_map[emotion_to_edit] = updated_genres
        st.success(f"Genres for '{emotion_to_edit}' updated successfully!")