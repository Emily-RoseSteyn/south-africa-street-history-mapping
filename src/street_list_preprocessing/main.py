import time

from street_list_preprocessing.get_country_street_files import get_country_street_files
from street_list_preprocessing.preprocess_country_streets import preprocess_country_streets
from utils.logger import get_logger

logger = get_logger()


def preprocess_streets() -> None:
    logger.info("Preprocess street list for countries")

    start_time = time.time()

    # Get a list of country street files
    countries = get_country_street_files()

    # For each file
    for country_file in countries:
        logger.info(
            f"File {country_file} is being processed"
        )

        preprocess_country_streets(country_file)

    # Finished
    logger.info(
        "Time spent in minutes: %s",
        int(time.time() - start_time) / 60,
    )


def main() -> None:
    preprocess_streets()


if __name__ == "__main__":
    main()
