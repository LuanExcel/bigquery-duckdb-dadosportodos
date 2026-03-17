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

    # ➡️ O DuckDB tentou ler uma VIEW
    # ➡️ A Storage API do BigQuery só permite ler TABELAS
    # ➡️ Lendo a View diretamente pelo bigquery
    consulta = client.query("""
    SELECT *
    FROM `projeto-desafios.views.vw_movies_kpis`
    LIMIT 10
    """).to_dataframe()

    print(consulta)

    sql = """
    CREATE OR REPLACE VIEW `projeto-desafios.views.vw_scatter_popularity_vs_quality` AS

    SELECT
    movieId,
    title,
    genres,
    release_year,
    total_ratings,
    avg_rating
    FROM `projeto-desafios.views.vw_movies_kpis`
    WHERE total_ratings >= 50
    """

    job = client.query(sql)
    job.result()

    print("View criada com sucesso!")

if __name__ == "__main__":
    consulta()

