import os
from pathlib import Path

import pandas as pd

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP


def preprocess_country_streets(country_file):

    # Determine iso code
    country = Path(os.path.basename(country_file)).stem
    country_code_map = COUNTRY_ISO_CODE_NAME_MAP
    iso_code = list(country_code_map.keys())[list(country_code_map.values()).index(country)]

    # * Load CSV
    df = pd.read_csv(country_file)

    # * Explode words
    # * Lowercase
    # * Aggregate (with frequency)
    # * Remove numbered words
    # * Figure out which words to remove completely (custom stop words)
    # * Remove stop words
    # * Save dataframe of specific street terms - term, country, country_iso_code
