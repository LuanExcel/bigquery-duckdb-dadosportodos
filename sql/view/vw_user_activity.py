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

    sql = """
    CREATE OR REPLACE VIEW `projeto-desafios.views.vw_user_activity` AS
    SELECT
        userId,
        COUNT(*) AS total_ratings,
        COUNT(DISTINCT movieId) AS distinct_movies_rated,
        AVG(rating) AS avg_rating,
        STDDEV(rating) AS std_rating,
        MIN(rating_ts) AS first_activity_ts,
        MAX(rating_ts) AS last_activity_ts
    FROM `projeto-desafios.analytics.fRating`
    GROUP BY userId
    """

    job = client.query(sql)
    job.result()

    print("View criada com sucesso!")

if __name__ == "__main__":
    consulta()

