import time

from utils.country_iso_map import COUNTRY_ISO_MAP
from street_list_download.download_country_streets import download_country_streets
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

        download_country_streets(country)

    # Finished
    logger.info(
        "Time spent in minutes: %s",
        int(time.time() - start_time) / 60,
    )


def main() -> None:
    retrieve_street_list()


if __name__ == "__main__":
    main()
