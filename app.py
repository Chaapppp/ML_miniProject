import streamlit as st

st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] ul {
            font-size: 17px !important;  
        }
            
        div[data-testid="stSidebarNav"] ul li {
            padding: 2px 2px !important;  
        }
        div[data-testid="stSidebarNav"] ul li:hover, 
        div[data-testid="stSidebarNav"] ul li:active {
            box-shadow: 0 0 5px #FF4B4B !important;  
            transition: box-shadow 0.4s ease-in-out        }
    </style>
""", unsafe_allow_html=True)

project_page_1 = st.Page(
    "pages/movie_recommend_page.py",
    title="Movie Recommendation",
    icon=":material/movie:",
)
project_page_2 = st.Page(    
    "pages/emotion_based_page.py",
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