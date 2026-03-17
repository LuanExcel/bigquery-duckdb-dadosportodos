import duckdb
from google.oauth2 import service_account
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

GCS_KEY_ID = os.getenv("GCS_KEY_ID")
GCS_SECRET = os.getenv("GCS_SECRET")

CREDENTIALS_FILE = "./gbq.json"
PROJECT_ID = "projeto-desafios"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE
)

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

    # =======================================================
    #  Lendo e criando tabela user_rating_history
    # =======================================================
    con.execute("""
    CREATE OR REPLACE TABLE user_rating_history AS
    SELECT *
    FROM read_csv(
        'gs://src-desafio01/bronze/user_rating_history.csv',
        all_varchar = TRUE
    );
    """)

    # =======================================================
    #  Lendo e criando tabela ratings_for_additional_users
    # =======================================================
    con.execute("""
    CREATE OR REPLACE TABLE ratings_for_additional_users AS
    SELECT *
    FROM read_csv(
        'gs://src-desafio01/bronze/ratings_for_additional_users.csv',
        all_varchar = TRUE
    );
    """)


    # =======================================================
    # Criando tabela fRating
    # CTE para unir tabela
    # Colocando a CTE dentro do CREATE pq CTE só existe nesse momento
    con.execute("""
    CREATE OR REPLACE TABLE bq.analytics.fRating AS
    WITH allratins AS (

    SELECT
        userId,
        movieId,
        TRY_CAST(NULLIF(NULLIF(rating,'NA'),'') AS DOUBLE) AS rating,
        TRY_STRPTIME(tstamp,'%Y-%m-%d %H:%M:%S') AS rating_ts,
        'user_rating_history' AS src
    FROM user_rating_history

    UNION ALL

    SELECT
        userId,
        movieId,
        TRY_CAST(NULLIF(NULLIF(rating,'NA'),'') AS DOUBLE) AS rating,
        TRY_STRPTIME(tstamp,'%Y-%m-%d %H:%M:%S') AS rating_ts,
        'ratings_for_additional_users' AS src
    FROM ratings_for_additional_users

    )

    SELECT
        userId,
        movieId,
        rating,
        rating_ts,
        src
    FROM allratins
    WHERE
        userId IS NOT NULL AND
        movieId IS NOT NULL AND
        rating IS NOT NULL AND
        rating_ts IS NOT NULL;
    """)

    df = con.execute("""
    SELECT *
    FROM bq.analytics.fRating
    LIMIT 10
    """).fetch_df()

    print(df)

    print("Tabela enviada para o BigQuery!")

if __name__ == "__main__":
    cadastro()

