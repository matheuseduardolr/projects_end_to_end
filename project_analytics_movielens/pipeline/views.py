import logging
import os
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
SQL_PATH = Path(__file__).resolve().parent.parent / "sql"

load_dotenv(env_path)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
bq_client = bigquery.Client(project=PROJECT_ID)


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


def create_views():
    try:
        views = [
            "views/vw_movie_kpis.sql",
            "views/vw_top_movies.sql",
            "views/vw_ratings_heatmap.sql",
            "views/vw_scatter_popularity_vs_quality.sql",
            "views/vw_user_activity.sql",
            "views/vw_genre_performance.sql",
        ]

        logging.info("Iniciando criação das views ")

        for view in views:
            try:
                logging.info(f"Criando view: {view}")
                run_sql(view)

            except Exception as e:
                logging.error(f"Erro ao criar view {view}: {e}", exc_info=True)

        logging.info("Criação de views finalizada ")

    except Exception as e:
        logging.error(f"Erro no processo de criação das views: {e}", exc_info=True)