import sqlite3

from street_list_preprocessing.get_country_street_files import get_country_street_files
from street_list_preprocessing.preprocess_country_streets import preprocess_country_streets
from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def preprocess_streets() -> None:
    logger.info("Preprocess street list for countries")

    # Remove previous results
    conn.execute(f"DROP TABLE IF EXISTS {MERGED_STREET_DATA_TABLE}")

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
    with conn:
        preprocess_streets()


if __name__ == "__main__":
    main()
