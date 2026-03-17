import duckdb
from google.oauth2 import service_account
from google.cloud import bigquery
import os

CREDENTIALS_FILE = "./gbq.json"
PROJECT_ID = "prejeto-desafios"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE
)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL bigquery FROM community; LOAD bigquery;")

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

def consulta():
    
    con.execute("""
    ATTACH 'project=prejeto-desafios' AS bq (TYPE bigquery)
    """)

    # ➡️ O DuckDB tentou ler uma VIEW
    # ➡️ A Storage API do BigQuery só permite ler TABELAS
    # ➡️ Lendo a View diretamente pelo bigquery
    consulta = client.query("""
    SELECT *
    FROM `prejeto-desafios.views.vw_movies_kpis`
    LIMIT 10
    """).to_dataframe()

    print(consulta)

    sql = """
    CREATE OR REPLACE VIEW `prejeto-desafios.views.vw_genre_performance` AS
    WITH exploded AS (
    SELECT
        r.rating,
        genre
    FROM `prejeto-desafios.analytics.fRating` r
    JOIN `prejeto-desafios.analytics.dMovies` m
        ON m.movieId = r.movieId
    CROSS JOIN UNNEST(SPLIT(COALESCE(m.genres, ''), '|')) AS genre
    )

    SELECT
    genre,
    COUNT(*) AS total_ratings,
    AVG(rating) AS avg_rating,
    STDDEV(rating) AS std_rating
    FROM exploded
    WHERE genre IS NOT NULL
    AND genre != ''
    AND genre != '(no genres listed)'
    GROUP BY genre
    ORDER BY total_ratings DESC, avg_rating DESC
    """


    job = client.query(sql)
    job.result()

    print("View criada com sucesso!")

if __name__ == "__main__":
    consulta()

