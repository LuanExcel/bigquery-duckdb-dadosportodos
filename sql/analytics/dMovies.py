import duckdb
from google.oauth2 import service_account
from google.cloud import bigquery
from dotenv import load_dotenv
import os

CREDENTIALS_FILE = "./gbq.json"
PROJECT_ID = "projeto-desafios"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE
)

load_dotenv()

GCS_KEY_ID = os.getenv("GCS_KEY_ID")
GCS_SECRET = os.getenv("GCS_SECRET")

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL bigquery FROM community; LOAD bigquery;")

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

def cadastro():

    con.execute(f"""
    CREATE SECRET (
        TYPE gcs,
        KEY_ID '{GCS_KEY_ID}',
        SECRET '{GCS_SECRET}'
    );
    """)

    con.execute("""
    ATTACH 'project=projeto-desafios' AS bq (TYPE bigquery)
    """)

    con.execute("""
    CREATE OR REPLACE TABLE movies AS
    SELECT *
    FROM read_csv(
    'gs://src-desafio01/bronze/movies.csv'
    );
    """)

    # ETL na tabela movies
    con.execute(r"""
    CREATE OR REPLACE TABLE dim_movies AS
    SELECT
        CAST(movieId AS VARCHAR) AS movieId,
        title,
        genres,
        TRY_CAST(REGEXP_EXTRACT(title, '\((\d{4})\)\s*$', 1) AS BIGINT) AS release_year
    FROM movies;
    """)

    # Mandando tabela pra o BigQuery
    con.execute("""
    CREATE OR REPLACE TABLE bq.analytics.dMovies AS
    SELECT *
    FROM dim_movies;
    """)

    print("Tabela enviada para o BigQuery!")

if __name__ == "__main__":
    cadastro()

