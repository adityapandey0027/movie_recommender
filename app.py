# import streamlit as st
# import pandas as pd
# import pickle

# # file_path = r"C:/Users/adity/Desktop/PROJECT/recomm/movies_list_dict.pkl"
# # with open("movie_list_dict.pkl", "rb") as f:
# #     movies = pickle.load(f)
# movies  = pd.read_csv("movies_list.csv")
# st.title("Movie Recommender System")

# option = st.selectbox(
#    "Here is available movie list ", 
# #    movies["title"].values
#     movies["title"].values
# )

import streamlit as st
import pandas as pd
import pickle
import requests
import time

import requests
import time

def fetch_poster_path(movie_id, retries=3, delay=0.1):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=062939b8b3eace4454d02b989c25cc7e&language=en-US"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        except Exception as e:
            print(f"Attempt {attempt+1} failed for movie_id {movie_id}: {e}")
            time.sleep(delay)
    
    # Final fallback after all retries fail
    return "https://via.placeholder.com/500x750?text=Error+Loading"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_list = []
    recommended_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_list.append(movies.iloc[i[0]].title)
        # time.sleep(0.1)  # delay for 200ms to avoid rate limiting
        recommended_poster.append(fetch_poster_path(movie_id))

    return recommended_list, recommended_poster


# Load the movies DataFrame from a CSV file
movies = pd.read_csv(r"C:\Users\adity\Desktop\PROJECT\recomm\movies_list.csv")
similarity = pickle.load(open(r"C:\Users\adity\Desktop\PROJECT\recomm\similar.pkl", "rb"))
st.title("Movie Recommender System")

selected_movie = st.selectbox(
   "Here is available movie list", 
   movies["title"].values
)

if st.button("Rocommend"):
    names, poster =recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
