import streamlit as st

project_page_1 = st.Page(
    "pages\movie_reccomendation_page.py",
    title="Movie Recommendation",
    icon=":material/movie:",
)
project_page_2 = st.Page(    
    "pages\emotion_page.py",
    title="Emotion-Based Recommendation",
    icon=":material/mood:",
    default=True,
)

pg = st.navigation(
    {
        "Movie Recommendation System": [project_page_1, project_page_2],
    }
)

pg.run()