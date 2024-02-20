import sqlite3
from typing import Any

from utils.env_variables import MERGED_STREET_DATA_TABLE, TERMS_DICTIONARY_TABLE


def drop_table(country: str, conn: sqlite3.Connection) -> None:
    conn.execute(f"DROP TABLE IF EXISTS {country}_{TERMS_DICTIONARY_TABLE}")


def create_table(country: str, conn: sqlite3.Connection):
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {country}_{TERMS_DICTIONARY_TABLE}"
        f"(term TEXT, frequency INTEGER, country TEXT, iso_code TEXT, likelihood REAL)")


def initialise_terms_table(country: str, conn: sqlite3.Connection, reset_db: bool = False) -> tuple[Any, int]:
    # Initialise db and table
    if reset_db:
        drop_table(country, conn)

    create_table(country, conn)

    # Reading merged street data from previous step
    total_terms = conn.execute(f"SELECT COUNT(*) FROM {MERGED_STREET_DATA_TABLE}").fetchone()[0]
    number_unique_countries = len(
        conn.execute(f"SELECT country FROM {MERGED_STREET_DATA_TABLE} GROUP BY country").fetchall())
    return total_terms, number_unique_countries
