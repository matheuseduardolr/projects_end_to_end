import logging
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound

PROJECT_ID = "vaulted-journal-489619-h7"
DATASET_ID = "movielens_raw"
BUCKET_NAME = "bucket-project-movielens"
PREFIX = "bronze/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bq_client = bigquery.Client(project=PROJECT_ID)
storage_client = storage.Client()

bucket = storage_client.bucket(BUCKET_NAME)
blobs = storage_client.list_blobs(bucket, prefix=PREFIX)

def external_tables():
    for blob in blobs:

        if not blob.name.endswith(".csv"):
            continue

        file_name = blob.name.split("/")[-1]
        table_base = file_name.replace(".csv", "")

        table_name = f"raw_{table_base}"
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

        try:
            bq_client.get_table(table_id)
            logging.info(f"--> Tabela já existia, pulando: {table_name} <--")
            continue

        except NotFound:
            pass

        external_config = bigquery.ExternalConfig("CSV")
        external_config.source_uris = [
            f"gs://{BUCKET_NAME}/{blob.name}"
        ]

        external_config.options.skip_leading_rows = 1
        external_config.autodetect = True

        table = bigquery.Table(table_id)
        table.external_data_configuration = external_config

        bq_client.create_table(table)

        logging.info(f"--> Tabela criada: {table_name} <--")
    
external_tables()