import os
from pathlib import Path

import requests

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP, COUNTRY_ISO_MAP
from utils.env_variables import STREET_DATA_DIR
from utils.logger import get_logger

logger = get_logger()


def download_country_streets(country_code: str) -> Path:
    country = COUNTRY_ISO_CODE_NAME_MAP[country_code]

    output_dir = STREET_DATA_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{country}.csv"
    path = Path.joinpath(Path(output_dir), filename)

    # Don't requery from overpass if file exists
    if os.path.exists(path):
        logger.info(
            f"Item {path} already exists - skipping download"
        )
        return path

    iso_standard = COUNTRY_ISO_MAP[country_code]
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:csv(name)];
    area["{iso_standard}"="{country_code}"];
    way(area)[highway][name];
    out;
    """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    with open(path, mode='wb') as file:
        file.write(response.content)
        file.close()
    return path