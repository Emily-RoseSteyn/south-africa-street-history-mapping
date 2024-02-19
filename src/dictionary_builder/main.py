import os
import sys

from street_list_preprocessing.get_country_street_files import get_country_street_files
from street_list_preprocessing.preprocess_country_streets import preprocess_country_streets
from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import MERGED_STREET_DATA_FILE
from utils.logger import get_logger

logger = get_logger()


def build_dictionary(country: str) -> None:
    logger.info(f"Building dictionary of street origins for country {country}")


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Please provide a country")
        return

    country = sys.argv[1]
    possible_countries = COUNTRY_ISO_CODE_NAME_MAP.values()

    if country in possible_countries:
        build_dictionary(country)
    else:
        output = ""
        for x in sorted(possible_countries):
            output = f"{output}- {x}\n"

        logger.error(f"Unknown country. Possible values are:\n{output}")
        return


if __name__ == "__main__":
    main()
