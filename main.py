from service.conexao_bq import upload_csv_gcs
from pathlib import Path

# Mandar bases csv para storage
def upload():

    pasta = Path("src")

    for arquivo in pasta.glob("*.csv"):

        upload_csv_gcs(
            bucket_name="src-desafio01",
            source_file=str(arquivo),
            destination_blob=f"bronze/{arquivo.name}"
        )

if __name__ == "__main__":
    upload()

