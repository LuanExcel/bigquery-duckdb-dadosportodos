import duckdb
from google.oauth2 import service_account
from google.cloud import bigquery
import os

CREDENTIALS_FILE = "./gbq.json"
PROJECT_ID = "projeto-desafios"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE
)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL bigquery FROM community; LOAD bigquery;")

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

def consulta():
    
    con.execute("""
    ATTACH 'project=projeto-desafios' AS bq (TYPE bigquery)
    """)

    consulta = con.execute("""
        SELECT *
        FROM bq.analytics.fRating
        LIMIT 10
    """).fetchdf()

    print(consulta)

    consulta = con.execute("""
        SELECT *
        FROM bq.analytics.dMovies
        LIMIT 10
    """).fetchdf()

    print(consulta)

    sql = """
    CREATE OR REPLACE VIEW `projeto-desafios.views.vw_movies_kpis` AS
    SELECT
        r.movieId,
        m.title,
        m.genres,
        m.release_year,
        COUNT(*) AS total_ratings,
        AVG(r.rating) AS avg_rating,
        STDDEV(r.rating) AS std_rating,
        MIN(r.rating_ts) AS first_rating_ts,
        MAX(r.rating_ts) AS last_rating_ts
    FROM `projeto-desafios.analytics.fRating` r
    LEFT JOIN `projeto-desafios.analytics.dMovies` m
        ON m.movieId = r.movieId
    GROUP BY
        r.movieId,
        m.title,
        m.genres,
        m.release_year;
    """

    job = client.query(sql)
    job.result()

    print("View criada com sucesso!")

if __name__ == "__main__":
    consulta()

