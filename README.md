# **Movie Recommendation System**

### Overview
This project is a **Movie Recommendation System** that provides movie suggestions based on user-selected movies and emotional states. The system includes two recommendation approaches:
1. **Content-Based Filtering**: Recommends movies similar to the selected ones.
2. **Emotion-Based Recommendation**: Suggests movies based on user emotions and associated genres.

The project is built using **Streamlit** for the web interface and uses a **preprocessed movie dataset** for recommendations.

### Dataset
The system uses the [TMDb 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv), which includes data like genres, cast, crew, and popularity scores. The dataset is preprocessed to extract relevant features for recommendation.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Chaapppp/ML_miniProject.git
    ```

2. Navigate into the project directory:
    ```bash
    cd ML_miniProject
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### Usage

1. Run the Jupyter notebooks to generate preprocessed model files:

   - `Emotion_Based_Recommendation_System.ipynb`
   
   - `Movie_Recommendation_System.ipynb`
   
   These notebooks generate `(movie_data.pkl, movie_emotion.pkl, lstm_movie_model.h5)` required for the recommendation system. 

3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

4. Open your web browser and go to `http://localhost:8501`.

### Application

- **Movie Recommendation Page**

1. Select up to 5 movies from the dropdown menu.
2. Click on "Recommend" to get your personalized movie recommendations.
3. View the recommended movies along with their posters.
4. Click "Get More Recommendations" to load additional recommendations.

- **Emotion-Based Recommendation Page**

1. Select an emotion from the available list.
2. Click on "Recommend" to get movie suggestions based on your mood.
3. View the recommended movies along with their posters.
4. Click "Get More Recommendations" to see additional movie recommendations.

### Model Architecture
The system consists of two main models:
- **Content-Based Filtering Model**: Uses cosine similarity on movie features to recommend similar movies.
- **Emotion-Based Model**: Maps emotions to specific genres and recommends movies accordingly using LSTM and cosine similarity.

    ![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20213352.png)


### Web Application
The web interface is built using **Streamlit**, and it includes two main pages:
1. **Movie Recommendation Page**
    - Allows users to select up to **5 movies**.
    - Generates recommendations based on content similarity.
    - Provides an option to get more recommendations.

![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20182506.png)

![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20192147.png)

![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20192216.png)

2. **Emotion-Based Recommendation Page**
    - Users select an emotion from a predefined list.
    - Suggests movies associated with the emotion's relevant genres.
    - Provides an option to get more recommendations.
   
![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20182524.png)

![Image](https://github.com/Chaapppp/ML_miniProject/blob/main/web%20sample/Screenshot%202025-03-09%20192247.png)
