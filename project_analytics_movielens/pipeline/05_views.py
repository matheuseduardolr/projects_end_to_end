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

def create_views():
    views = [
        "views/vw_movie_kpis.sql",
        "views/vw_top_movies.sql",
        "views/vw_ratings_heatmap.sql",
        "views/vw_scatter_popularity_vs_quality.sql",
        "views/vw_user_activity.sql",
        "views/vw_genre_performance.sql",
    ]

    for view in views:
        logging.info(f"Criando view: {view}")
        run_sql(view)

create_views()