from pipeline.extract import extract_sources
from pipeline.load import upload_sources_to_gcs
from pipeline.external_tables import create_external_tables
from pipeline.analytics_tables import create_analytical_tables
from pipeline.views import create_views
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    try:
        extract_sources()
        upload_sources_to_gcs()
        create_external_tables()
        create_analytical_tables()
        create_views()

    except Exception as e:
        logging.error(f"Erro durante a execução do pipeline: {e}", exc_info=True)


if __name__ == "__main__":
    main()