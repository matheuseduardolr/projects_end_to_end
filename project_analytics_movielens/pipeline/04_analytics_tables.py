import logging
import os
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
SQL_PATH = Path(__file__).resolve().parent.parent / "sql"

load_dotenv(env_path)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")

bq_client = bigquery.Client(project=PROJECT_ID)



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_sql(file_name: str):
    sql_file = SQL_PATH / file_name

    with open(sql_file) as f:
        query = f.read()

    query = query.replace("${PROJECT_ID}", PROJECT_ID)

    bq_client.query(query).result()

    logging.info(f"Query executada: {file_name}")


def create_dimensions():
    run_sql("dimensions/dim_movies.sql")


def create_facts():
    run_sql("facts/fact_ratings.sql")


def transform():
    create_dimensions()
    create_facts()

transform()