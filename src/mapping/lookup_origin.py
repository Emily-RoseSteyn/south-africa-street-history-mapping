import sqlite3

import pandas as pd

from mapping.country_colour_map import get_colour
from mapping.stop_terms import STOP_TERMS
from utils.env_variables import SQLITE_DB, TERMS_DICTIONARY_TABLE

conn = sqlite3.connect(SQLITE_DB)


def lookup_origin(street_name: str, country: str = "south_africa") -> str | None:
    street_name = street_name.lower()
    terms = street_name.split(' ')
    primary_terms = [i for i in terms if i not in STOP_TERMS]

    # Find any matching terms, select highest likelihood
    result = pd.read_sql_query(
        f"SELECT * FROM {country}_{TERMS_DICTIONARY_TABLE} "
        f"WHERE term in ({','.join(['?'] * len(primary_terms))}) "
        f"GROUP BY term "
        f"ORDER BY max(likelihood) DESC "
        f"LIMIT 1",
        conn,
        params=primary_terms)

    if result.empty:
        return None
    return result["country"][0]


def map_street_to_origin(x):
    street_name = x["name"]
    if isinstance(street_name, str):
        origin = lookup_origin(street_name)
        x["origin"] = origin
    else:
        x["origin"] = None
    x["colour"] = get_colour(x["origin"])

    return x
