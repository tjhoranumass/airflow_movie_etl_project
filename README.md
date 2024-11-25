# Airflow Movie ETL Project

This project demonstrates an ETL pipeline using Apache Airflow. The pipeline extracts movie data from the TMDb API, transforms the data by cleaning and enriching it, and loads it into a PostgreSQL database.

## Prerequisites

- Python 3.7+
- Apache Airflow
- PostgreSQL
- TMDb API Key

## Setup

1. Clone this repository.
2. Install the required dependencies:
   ```
   pip install apache-airflow pandas requests psycopg2-binary
    pip install apache-airflow-providers-postgres
   ```
3. Set up Apache Airflow:
   - Initialize the database:
     ```
     airflow db init
     airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
     ```
   - Start the webserver and scheduler:
     ```
     airflow webserver --port 8080
     airflow scheduler
     ```
4. Configure a PostgreSQL connection in Airflow:
   - Go to the Airflow web interface.
   - Add a new connection (`postgres_default`) with the details of your PostgreSQL database.

5. Replace `your_api_key` in `movie_etl.py` with your TMDb API key.

## Running the Pipeline

1. Place the `movie_etl.py` file in the Airflow `~/airflow/dags` directory.
2. Start the Airflow scheduler and webserver.
3. Trigger the DAG from the Airflow web interface.

## Output

The transformed movie data will be loaded into the `movies` table in your PostgreSQL database.

## Database Schema

```sql
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    release_date DATE,
    genre VARCHAR(255),
    average_rating FLOAT,
    vote_count INT
);
```

## License

This project is licensed under the MIT License.
