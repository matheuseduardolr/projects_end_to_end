from pathlib import Path
import logging
from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

BUCKET_NAME = "bucket-project-movielens"
GCS_FOLDER = "bronze"

def upload_sources_to_gcs():
    try:
        logging.info("Iniciando upload das fontes para GCS ")

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)

        csv_files = list(DATA_DIR.glob("*.csv"))

        if not csv_files:
            logging.warning("Nenhum arquivo CSV encontrado para upload ")
            return

        for file in csv_files:
            try:
                blob_path = f"{GCS_FOLDER}/{file.name}"
                blob = bucket.blob(blob_path)

                if blob.exists(client):
                    logging.info(f"Upload skipped: {file.name} ")
                    continue

                blob.upload_from_filename(file)
                logging.info(f"Upload realizado: {file.name} ")

            except Exception as e:
                logging.error(f"Erro ao enviar {file.name} para o GCS: {e}", exc_info=True)

        logging.info("Upload finalizado com sucesso. ")

    except Exception as e:
        logging.error(f"Erro ao iniciar processo de upload para GCS: {e}", exc_info=True)