import logging
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
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


def get_schema_from_csv(blob):
    try:
        header = blob.download_as_text().split("\n")[0]
        columns = header.split(",")

        schema = []

        for col in columns:
            clean_col = col.strip().replace('"', '')
            schema.append(bigquery.SchemaField(clean_col, "STRING"))

        return schema

    except Exception as e:
        logging.error(f"Erro ao gerar schema do arquivo {blob.name}: {e}", exc_info=True)
        raise


def create_external_tables():

    try:
        logging.info("Iniciando criação de tabelas externas ")

        for blob in blobs:

            try:

                if not blob.name.endswith(".csv"):
                    continue

                file_name = blob.name.split("/")[-1]
                table_base = file_name.replace(".csv", "")

                table_name = f"raw_{table_base}"
                table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

                try:
                    bq_client.get_table(table_id)
                    logging.info(f" Tabela já existia, pulando: {table_name} ")
                    continue

                except NotFound:
                    pass

                schema = get_schema_from_csv(blob)

                external_config = bigquery.ExternalConfig("CSV")
                external_config.source_uris = [
                    f"gs://{BUCKET_NAME}/{blob.name}"
                ]

                external_config.options.skip_leading_rows = 1
                external_config.autodetect = False

                table = bigquery.Table(table_id, schema=schema)
                table.external_data_configuration = external_config

                bq_client.create_table(table)

                logging.info(f"Tabela criada: {table_name} ")

            except Exception as e:
                logging.error(f"Erro ao criar tabela para {blob.name}: {e}", exc_info=True)

        logging.info("Criação de tabelas externas finalizada ")

    except Exception as e:
        logging.error(f"Erro no processo de criação de tabelas externas: {e}", exc_info=True)