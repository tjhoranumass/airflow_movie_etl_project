from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime
import requests
import pandas as pd

def fetch_movie_data():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": "bb5417952b55ccc4237c7f911fe17d41"}
    response = requests.get(url, params=params)
    with open('~/movies.json', 'w') as f:
        f.write(response.text)

def transform_movie_data():
    df = pd.read_json('/tmp/movies.json')
    movies = df['results']
    df = pd.json_normalize(movies)
    df = df[['title', 'release_date', 'genre_ids', 'vote_average', 'vote_count']]
    df = df.rename(columns={'vote_average': 'average_rating'})
    df = df.dropna()
    df.to_csv('~/movies_transformed.csv', index=False)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG('movie_etl', default_args=default_args, schedule_interval='@daily')

extract_task = PythonOperator(
    task_id='fetch_movie_data',
    python_callable=fetch_movie_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_movie_data',
    python_callable=transform_movie_data,
    dag=dag,
)

load_task = PostgresOperator(
    task_id='load_movie_data',
    postgres_conn_id='movies_airflow',
    sql="""
        COPY movies (title, release_date, genre, average_rating, vote_count)
        FROM '~/movies_transformed.csv'
        DELIMITER ','
        CSV HEADER;
    """,
    dag=dag,
)

extract_task >> transform_task >> load_task
