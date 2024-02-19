import os

from street_list_preprocessing.get_country_street_files import get_country_street_files
from street_list_preprocessing.preprocess_country_streets import preprocess_country_streets
from utils.env_variables import MERGED_STREET_DATA_FILE
from utils.logger import get_logger

logger = get_logger()


def preprocess_streets() -> None:
    logger.info("Preprocess street list for countries")

    # Remove previous results
    output_file = MERGED_STREET_DATA_FILE
    if os.path.exists(output_file):
        os.remove(output_file)

    # Get a list of country street files
    countries = get_country_street_files()

    # For each file
    for country_file in countries:
        preprocess_country_streets(country_file)

    # Finished
    logger.info(
        "Done",
    )


def main() -> None:
    preprocess_streets()


if __name__ == "__main__":
    main()
