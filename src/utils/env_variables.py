# env_variables.py

"""This module defines project-level env variable keys."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

WORD_LENGTH_THRESHOLD = 3
FUZZY_MATCH_THRESHOLD = 80

STREET_DATA_DIR = "data/streets"
PROCESSED_STREET_DATA_DIR = "output/streets"

STREET_OUTPUT_PREFIX = "processed"

MERGED_STREET_DATA_FILE = "output/street_terms.csv"
TERMS_DICTIONARY = "terms_dictionary.csv"

SQLITE_DB = "output/street_history.sqlite"
TERMS_DICTIONARY_TABLE = "terms_dictionary"
