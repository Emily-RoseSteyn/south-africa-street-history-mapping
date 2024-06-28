import sqlite3
from typing import Any

import pandas as pd

from lookup_language.lookup_word import LanguageDetector
from mapping.stop_terms import STOP_TERMS
from utils.env_variables import SQLITE_DB, TERMS_DICTIONARY_TABLE, TERMS_LANGUAGE_DICTIONARY_TABLE

conn = sqlite3.connect(SQLITE_DB)


def lookup_origin(street_name: str, map_language: bool = False, country: str = "south_africa"
                  ) -> tuple[None, None] | tuple[Any, Any]:
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
        return None, None

    primary_term = result["term"][0]
    origin = result["country"][0]

    if map_language and origin == country:
        # Do an additional language lookup
        # Find any matching terms, select highest likelihood
        language_result = pd.read_sql_query(
            f"SELECT * FROM {TERMS_LANGUAGE_DICTIONARY_TABLE} "
            f"WHERE term = ?"
            f"ORDER BY likelihood DESC "
            f"LIMIT 1",
            conn,
            params=[primary_term])
        origin = language_result["language"][0]

    return origin, primary_term


def lookup_language(street_name: str) -> tuple[None, None] | tuple[Any, Any]:
    street_name = street_name.lower()
    terms = street_name.split(' ')
    primary_terms = [i for i in terms if i not in STOP_TERMS]

    primary_term = ' '.join(primary_terms)

    # Do language lookup
    # Find any matching terms, select highest likelihood
    language_detector = LanguageDetector()
    language_result = language_detector.detect(primary_term)
    origin = language_result["language"][0]

    return origin, primary_term


def map_street_to_origin(x, map_language: bool = False):
    street_name = x["name"]
    if map_language and isinstance(street_name, str):
        origin, primary_term = lookup_language(street_name)
        x["origin"] = origin
        x["primary_term"] = primary_term
    elif isinstance(street_name, str):
        origin, primary_term = lookup_origin(street_name, map_language)
        x["origin"] = origin
        x["primary_term"] = primary_term
    else:
        x["origin"] = None
        x["primary_term"] = None
        x["name"] = None

    return x
