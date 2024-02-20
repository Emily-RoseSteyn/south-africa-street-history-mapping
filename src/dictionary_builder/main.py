import sqlite3
import sys

import pandas as pd
from tqdm import tqdm

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import SQLITE_DB, \
    TERMS_DICTIONARY_TABLE, MERGED_STREET_DATA_TABLE
from utils.logger import get_logger

logger = get_logger()

conn = sqlite3.connect(SQLITE_DB)


def initialise_db(country: str) -> None:
    conn.execute(f"DROP TABLE IF EXISTS {country}_{TERMS_DICTIONARY_TABLE}")


def term_exists(country: str, term: str) -> bool:
    result = conn.execute(f"SELECT * FROM {country}_{TERMS_DICTIONARY_TABLE} WHERE term = ? LIMIT 1",
                          (term,)).fetchone()
    return result is not None


def write_df_to_sql(country: str, df: pd.DataFrame) -> None:
    df.to_sql(f"{country}_{TERMS_DICTIONARY_TABLE}", conn, if_exists='append', index=False)


def build_dictionary(country: str, reset_db: bool = False) -> None:
    logger.info(f"Building dictionary of street origins for country {country}")

    # Reading merged street data from previous step
    terms_df = pd.read_sql_query(f"SELECT * FROM {MERGED_STREET_DATA_TABLE}", conn)

    # Initialise db and table
    if reset_db:
        initialise_db(country)

    # Separate terms by country being processed
    country_terms = terms_df[terms_df["country"] == country]

    # Decided to not remove the country being processed
    # terms_df = terms_df[terms_df["country"] != country]
    number_unique_countries = len(terms_df["country"].unique())
    logger.info(
        f"Comparing {len(country_terms)} terms from {country} to {len(terms_df)} terms from " +
        f"{number_unique_countries} countries (including {country})")

    # Favour exact match over fuzzy
    for term in tqdm(country_terms["term"]):
        # Skip if term already exists
        if term_exists(country, term):
            continue

        # Any ways to speed up processing?
        exact_match = terms_df[terms_df["term"] == term]
        number_matches = len(exact_match)

        # TODO: If term not found
        #  this is impossible because of the lookup of the country to oneself
        if number_matches == 0:
            continue

        if number_matches == 1:
            exact_match = exact_match.assign(likelihood=[100])

        # If more than one exact match, work out countries to retain
        if number_matches > 1:
            likelihoods = exact_match["frequency"] * 100 / exact_match["frequency"].sum()
            exact_match = exact_match.assign(likelihood=likelihoods)
            # Write all exact matches to sqlite
            # exact_match = exact_match.sort_values(by=["likelihood"], ascending=False).reset_index(drop=True)
            # threshold_index = exact_match['likelihood'].cumsum().gt(threshold).idxmin() + 1
            # exact_match = exact_match.loc[:threshold_index]

        write_df_to_sql(country, exact_match)


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Please provide a country")
        return

    country = sys.argv[1]
    possible_countries = COUNTRY_ISO_CODE_NAME_MAP.values()

    if country in possible_countries:
        with conn:
            build_dictionary(country)
    else:
        output = ""
        for x in sorted(possible_countries):
            output = f"{output}- {x}\n"

        logger.error(f"Unknown country. Possible values are:\n{output}")
        return


if __name__ == "__main__":
    main()
