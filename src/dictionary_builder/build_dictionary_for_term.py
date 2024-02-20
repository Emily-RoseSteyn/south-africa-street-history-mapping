import sqlite3

import pandas as pd

from utils.env_variables import TERMS_DICTIONARY_TABLE, MERGED_STREET_DATA_TABLE


def term_exists(country: str, term: str, conn: sqlite3.Connection) -> bool:
    try:
        result = conn.execute(f"SELECT * FROM {country}_{TERMS_DICTIONARY_TABLE} WHERE term = ? LIMIT 1",
                              (term,)).fetchone()
        return result is not None
    except sqlite3.OperationalError:
        return False


def match_term(term: str, conn: sqlite3.Connection):
    # Decided to not remove the country being processed
    return pd.read_sql(f"SELECT * FROM {MERGED_STREET_DATA_TABLE} WHERE term = ?", conn,
                       params=[term])


def write_df_to_sql(country: str, df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    df.to_sql(f"{country}_{TERMS_DICTIONARY_TABLE}", conn, if_exists='append', index=False)


def build_dictionary_for_term(
        country: str, term: str, conn: sqlite3.Connection) -> None:
    # Skip if term already exists
    if term_exists(country, term, conn):
        return

    # Query sql
    exact_match = match_term(term, conn)
    number_matches = len(exact_match)

    # TODO: If term not found
    #  this is impossible because of the lookup of the country to oneself
    if number_matches == 0:
        return

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

    write_df_to_sql(country, exact_match, conn)
