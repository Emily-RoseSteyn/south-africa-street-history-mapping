import sqlite3

import pandas as pd
from tqdm import tqdm

from dictionary_builder.build_dictionary_for_term import build_dictionary_for_term
from dictionary_builder.extract_country_from_args import extract_country
from dictionary_builder.initialise_terms_table import initialise_terms_table
from utils.env_variables import SQLITE_DB, \
    MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def build_dictionary(country: str, reset_db: bool = False) -> None:
    logger.info(f"Building dictionary of street origins for country {country}")

    total_terms, number_unique_countries = initialise_terms_table(country, conn, reset_db)

    # Separate terms by country being processed
    country_terms = pd.read_sql_query(f"SELECT * FROM {MERGED_STREET_DATA_TABLE} WHERE country = ?", conn,
                                      params=[country])

    logger.info(
        f"Comparing {len(country_terms)} terms from {country} to {total_terms} terms from " +
        f"{number_unique_countries} countries (including {country})")

    # Favour exact match over fuzzy
    for term in tqdm(country_terms["term"]):
        build_dictionary_for_term(country, term, conn)


def main() -> None:
    country = extract_country()
    if country is None:
        return

    with conn:
        build_dictionary(country)


if __name__ == "__main__":
    main()
