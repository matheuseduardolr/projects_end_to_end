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
    try:
        sql_file = SQL_PATH / file_name

        with open(sql_file) as f:
            query = f.read()

        query = query.replace("${PROJECT_ID}", PROJECT_ID)

        bq_client.query(query).result()

        logging.info(f"Query executada: {file_name}")

    except FileNotFoundError:
        logging.error(f"Arquivo SQL não encontrado: {file_name}", exc_info=True)

    except Exception as e:
        logging.error(f"Erro ao executar query {file_name}: {e}", exc_info=True)
        raise


def create_dimensions():
    try:
        run_sql("dimensions/dim_movies.sql")
    except Exception as e:
        logging.error(f"Erro na criação da dimensão dim_movies: {e}", exc_info=True)
        raise


def create_facts():
    try:
        run_sql("facts/fact_ratings.sql")
    except Exception as e:
        logging.error(f"Erro na criação da tabela fato fact_ratings: {e}", exc_info=True)
        raise


def create_analytical_tables():
    try:
        logging.info(" Criando tabelas analíticas ")

        create_dimensions()
        create_facts()

        logging.info(" Tabelas analíticas criadas com sucesso ")

    except Exception as e:
        logging.error(f"Erro na criação das tabelas analíticas: {e}", exc_info=True)
        raise