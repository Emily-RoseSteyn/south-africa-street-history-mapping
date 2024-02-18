import os
from pathlib import Path

import requests

from street_list_retrieval.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP, COUNTRY_ISO_MAP


def fetch_streets_for_country_code(country_code: str):
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
    country = COUNTRY_ISO_CODE_NAME_MAP[country_code]

    output_dir = "./data/streets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{country}.csv"
    path = Path.joinpath(Path(output_dir), filename)

    with open(path, mode='wb') as file:
        file.write(response.content)
        file.close()
    return path


def retrieve_and_process_country(country_code: str) -> None:
    fetch_streets_for_country_code(country_code)


if __name__ == "__main__":
    retrieve_and_process_country()
