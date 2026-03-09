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
    logging.info("---> Iniciando upload das fontes para GCS <---")

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    csv_files = list(DATA_DIR.glob("*.csv"))

    for file in csv_files:
        blob_path = f"{GCS_FOLDER}/{file.name}"
        blob = bucket.blob(blob_path)

        if blob.exists(client):
            logging.info(f"---> Upload skipped: {file.name} <---")
            continue

        blob.upload_from_filename(file)
        logging.info(f"---> Upload realizado: {file.name} <---")

    logging.info(f"---> Upload finalizado com sucesso. <---")

upload_sources_to_gcs()
