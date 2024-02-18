import time

from street_list_retrieval.country_iso_map import COUNTRY_ISO_MAP, COUNTRY_ISO_CODE_NAME_MAP
from street_list_retrieval.retrieve_and_process_country import retrieve_and_process_country
from utils.logger import get_logger

logger = get_logger()


def retrieve_street_list() -> None:
    logger.info("Retrieving street list for countries")

    start_time = time.time()

    # Get a list of countries
    countries = COUNTRY_ISO_MAP.keys()

    # For each file
    for country in countries:
        logger.info(
            f"Item {country} is being processed"
        )

        retrieve_and_process_country(country)

    # Finished
    logger.info(
        "Time spent in minutes: %s",
        int(time.time() - start_time) / 60,
    )


def main() -> None:
    retrieve_street_list()


if __name__ == "__main__":
    main()
