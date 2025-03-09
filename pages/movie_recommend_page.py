import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations from multiple movies
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

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

# Streamlit UI
st.title("Movie Recommendation System")

# Session state to store selected movies and recommendation index
if 'selected_movies' not in st.session_state:
    st.session_state.selected_movies = []
if 'rec_index' not in st.session_state:
    st.session_state.rec_index = 0
if 'show_more_button' not in st.session_state:
    st.session_state.show_more_button = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = pd.DataFrame()  # Initialize as an empty DataFrame

# **Force Reset Button State on Page Load**
if st.session_state.recommendations.empty:
    st.session_state.show_more_button = False  # Hide button if no recommendations exist
   
# Add placeholder option to movie selection dropdown
selected_movie = st.selectbox("Select a movie:", movies['title'].values, index=None)

left_column, right_column = st.columns([5.8, 1])  # Adjust column width as needed

with right_column:
    # Add movie button
    if st.button("Add Movie"):
        if selected_movie is not None:
            if selected_movie not in st.session_state.selected_movies and len(st.session_state.selected_movies) < 5:
                st.session_state.selected_movies.append(selected_movie)

# Display selected movies with posters centered
st.subheader("Selected Movies:")
if st.session_state.selected_movies:
    num_movies = len(st.session_state.selected_movies)
    selected_cols = st.columns(5)  # Create fixed 5 columns
    start_col = 0  
    for i, movie in enumerate(st.session_state.selected_movies):
        col = selected_cols[start_col + i]  
        movie_id = movies[movies['title'] == movie]['movie_id'].values[0]
        poster_url = fetch_poster(movie_id)
        with col:
            if poster_url:
                st.image(poster_url, width=130)
            st.markdown(f"<div align='center'>{movie}</div>", unsafe_allow_html=True)
else:
    st.write("No movie selected.")

st.write("\n")  # Add space 
left_column1, left_column2, right_column1, right_column2 = st.columns([8, 4.2, 2, 3]) 

with right_column1:
    # Undo selected movies
    if st.button("Undo"):
        if st.session_state.selected_movies:
            st.session_state.selected_movies.pop()
            st.session_state.rec_index = 0  # Reset recommendation index
            st.session_state.show_more_button = False
            st.rerun()

with right_column2:
    # Clear all selected movies
    if st.button("Clear Movies"):
        st.session_state.selected_movies = []
        st.session_state.rec_index = 0  # Reset recommendation index
        st.session_state.show_more_button = False
        st.rerun()

col1, col2 = st.columns([5.4, 1.1])  # Adjust column width as needed

# Recommend movies button
with col2:
    recommendations_clicked = st.button("Recommend")

if recommendations_clicked:
    if not st.session_state.selected_movies:
        st.warning("Please add at least one movie.")
    else:
        st.session_state.rec_index = 0  # Reset recommendation index
        recommendations = get_recommendations(st.session_state.selected_movies)

        if recommendations.empty:
            st.error("No recommendations found. Try selecting different movies.")
        else:
            st.session_state.show_more_button = True  # Show the Get More Recommendations button
            st.session_state.recommendations = recommendations  # Store recommendations
            st.subheader("Top 10 Recommended Movies:")
            for i in range(0, len(recommendations), 5):  # Display in rows of 5
                cols = st.columns(5)
                st.write("\n")  # Add space 
                for col, j in zip(cols, range(i, i+5)):
                    if j < len(recommendations):
                        movie_title = recommendations.iloc[j]['title']
                        movie_id = recommendations.iloc[j]['movie_id']
                        poster_url = fetch_poster(movie_id)
                        with col:
                            if poster_url:
                                st.image(poster_url, width=130)
                            st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True)

# Re-Recommendation Button 
if st.session_state.get("show_more_button", False) and not st.session_state.recommendations.empty:
    with col1:
        if st.session_state.get('show_more_button', False):
            re_recommendations_clicked = st.button("Get More Recommendations", key="get_more")
            
    if "show_more_button" in st.session_state and st.session_state.show_more_button and re_recommendations_clicked:
                if not st.session_state.selected_movies:
                    st.warning("Please add at least one movie.")
                else:
                    st.session_state.rec_index += 10  # Increment to get the next 10 recommendations
                    recommendations = get_recommendations(st.session_state.selected_movies, start_index=st.session_state.rec_index)
                    
                    if recommendations.empty:
                        st.session_state.rec_index = 0  # Reset if no more recommendations available
                        recommendations = get_recommendations(st.session_state.selected_movies, start_index=st.session_state.rec_index)
                    
                    st.subheader("More Recommended Movies:")
                    for i in range(0, len(recommendations), 5):  # Display in rows of 5
                        cols = st.columns(5)
                        st.write("\n")  # Add space 
                        for col, j in zip(cols, range(i, i+5)):
                            if j < len(recommendations):
                                movie_title = recommendations.iloc[j]['title']
                                movie_id = recommendations.iloc[j]['movie_id']
                                poster_url = fetch_poster(movie_id)
                                with col:
                                    if poster_url:
                                        st.image(poster_url, width=130)
                                    st.markdown(f"<div align='center'>{movie_title}</div>", unsafe_allow_html=True)