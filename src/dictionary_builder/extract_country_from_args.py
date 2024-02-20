import sys

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.logger import get_logger

logger = get_logger()


def extract_country() -> str | None:
    if len(sys.argv) < 2:
        logger.error("Please provide a country")
        return None

    country = sys.argv[1]
    possible_countries = COUNTRY_ISO_CODE_NAME_MAP.values()

    if country in possible_countries:
        return country
    else:
        output = ""
        for x in sorted(possible_countries):
            output = f"{output}- {x}\n"

        logger.error(f"Unknown country. Possible values are:\n{output}")
        return None
