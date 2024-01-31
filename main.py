import pandas as pd
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="Movie Recommender App",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

background_image = 'darkthreater.jpg'
html_code = f"""
    <style>
        body {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .stApp {{
            background: none;  /* Remove Streamlit app background */
        }}
    </style>
"""

# Apply the styling with the background image
st.markdown(html_code, unsafe_allow_html=True)

# Load data
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
data = pd.read_csv('movie.data', sep='\t', names=column_names)
mov_titles = pd.read_csv('Movie_Id_Titles')
df = pd.merge(data, mov_titles, on='item_id')

# Calculate ratings and create a movie matrix
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['no_of_ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
moviemat = df.pivot_table(index='user_id', columns='title', values='rating')

# Function to recommend movies
def mov_recommender(movie, threshold=100):
    movie_ratings = moviemat[movie]
    similar_movies = moviemat.corrwith(movie_ratings)
    corr_movie = pd.DataFrame(similar_movies, columns=['Correlation'])
    corr_movie.dropna(inplace=True)
    corr_movie = corr_movie.join(ratings['no_of_ratings'])
    recommended_movies = corr_movie[corr_movie['no_of_ratings'] > threshold].sort_values('Correlation', ascending=False)
    recommended_titles = recommended_movies.index.to_list()  # Extract only movie titles
    return recommended_titles

# Streamlit app

# Header
st.title("🎬 Movie Recommender App")
st.markdown("Welcome to the Movie Recommender App! Embark on a cinematic journey and discover your next favorite films.")

# Sidebar
st.sidebar.header("Your Movie Preferences")
movie_input = st.sidebar.selectbox('Select a movie:', mov_titles['title'].to_list(), index=None)
threshold = st.sidebar.slider("Set the minimum number of ratings:", min_value=50, max_value=500, value=100)

if movie_input:
    recommended_titles = mov_recommender(movie_input, threshold)
    
    st.subheader(f'Recommended Movies for "{movie_input}":')
    st.table(pd.DataFrame({'Recommended Movies': recommended_titles[:11]})[1:])
else:
    st.warning('Please select a movie.')
# --------------------------------------------------------------------------------------------------------------
