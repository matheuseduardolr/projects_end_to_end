import requests
from pathlib import Path
import logging
import zipfile

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

data_dir = Path(__file__).resolve().parent.parent / "data"
zip_path = data_dir / "movielens_sources.zip"

def extract_sources():
    try:
        logging.info("Iniciando download das fontes ")

        data_dir.mkdir(parents=True, exist_ok=True)

        if zip_path.exists():
            logging.info("Fontes já foram extraídas anteriormente ")
            return

        url = "https://files.grouplens.org/datasets/movielens/ml_belief_2024_data_release_2.zip"

        response = requests.get(url)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(response.content)

        logging.info("Zip salvo com sucesso ")

        with zipfile.ZipFile(zip_path) as zip_ref:
            for file in zip_ref.namelist():

                if "data_release/" in file and file.endswith(".csv"):

                    filename = Path(file).name
                    target_path = data_dir / filename

                    with zip_ref.open(file) as source, open(target_path, "wb") as target:
                        target.write(source.read())

        logging.info("CSVs extraídos com sucesso ")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar o arquivo: {e}", exc_info=True)

    except zipfile.BadZipFile as e:
        logging.error(f"Erro ao descompactar o arquivo ZIP: {e}", exc_info=True)

    except Exception as e:
        logging.error(f"Erro inesperado durante a extração das fontes: {e}", exc_info=True)