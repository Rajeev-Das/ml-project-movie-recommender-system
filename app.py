import streamlit as st
import pickle
import requests

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dataframe = pickle.load(open('movies.pkl', 'rb'))


def fetch_poster(movie_id):
    api_key_tmdb = '779169ff1451c7667620f6fdae1bffb4'
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,
                                                                                                     api_key_tmdb))
    data = response.json()
    # st.write(data['poster_path'])
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']


def recommend(movie):
    movies_index = movies_dataframe[movies_dataframe['title'] == movie].index[0]
    distances = similarity[movies_index]
    list_of_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    movies_recommended = []
    posters = []
    for i in list_of_movies:
        # Append the movie names
        movies_recommended.append(movies_dataframe.iloc[i[0]].title)
        # Fetch the movie posters
        movie_id = movies_dataframe.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
    return movies_recommended, posters


movies_list = movies_dataframe['title'].values
st.title('Movie Recommender System')

option = st.selectbox('Movie for which you need the Top 5 Recommendations', movies_list)

if st.button('Recommend'):
    movie_names, movie_posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        st.subheader(movie_names[0])
        st.image(movie_posters[0], use_column_width=True)
    with col2:
        st.subheader(movie_names[1])
        st.image(movie_posters[1], use_column_width=True)
    with col3:
        st.subheader(movie_names[2])
        st.image(movie_posters[2], use_column_width=True)
    with col4:
        st.subheader(movie_names[3])
        st.image(movie_posters[3], use_column_width=True)
    with col5:
        st.subheader(movie_names[4])
        st.image(movie_posters[4], use_column_width=True)
