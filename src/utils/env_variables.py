# env_variables.py

"""This module defines project-level env variable keys."""
import logging
import os

from dotenv import load_dotenv

from utils.enum import enum

load_dotenv()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

WORD_LENGTH_THRESHOLD = 3
FUZZY_MATCH_THRESHOLD = 80

STREET_DATA_DIR = "data/streets"
PROCESSED_STREET_DATA_DIR = "output/streets"

SQLITE_DB = "output/street_history.sqlite"
TERMS_DICTIONARY_TABLE = "terms_dictionary"
MERGED_STREET_DATA_TABLE = "street_terms"

MPI_TAGS = enum('READY', 'DONE', 'EXIT', 'START')