import sqlite3
import sys

import pandas as pd
from tqdm import tqdm

from dictionary_builder.build_dictionary_for_term import build_dictionary_for_term
from dictionary_builder.extract_country_from_args import extract_country
from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import SQLITE_DB, \
    TERMS_DICTIONARY_TABLE, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def drop_table(country: str) -> None:
    conn.execute(f"DROP TABLE IF EXISTS {country}_{TERMS_DICTIONARY_TABLE}")


def build_dictionary(country: str, reset_db: bool = False) -> None:
    logger.info(f"Building dictionary of street origins for country {country}")

    # Initialise db and table
    if reset_db:
        drop_table(country)

    # Reading merged street data from previous step
    total_terms = conn.execute(f"SELECT COUNT(*) FROM {MERGED_STREET_DATA_TABLE}").fetchone()[0]
    number_unique_countries = len(
        conn.execute(f"SELECT country FROM {MERGED_STREET_DATA_TABLE} GROUP BY country").fetchall())

    # Separate terms by country being processed
    country_terms = pd.read_sql_query(f"SELECT * FROM {MERGED_STREET_DATA_TABLE} WHERE country = ?", conn,
                                      params=[country])

    logger.info(
        f"Comparing {len(country_terms)} terms from {country} to {total_terms} terms from " +
        f"{number_unique_countries} countries (including {country})")

    # Favour exact match over fuzzy
    for term in tqdm(country_terms["term"]):
        build_dictionary_for_term(country, term)


def main() -> None:
    country = extract_country()
    if country is None:
        return

    with conn:
        build_dictionary(country)


if __name__ == "__main__":
    main()
