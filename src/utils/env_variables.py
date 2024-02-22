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
OUTPUT_IMAGES_DIR = "output/images"
OUTPUT_GDF_DIR = "output/geojson"
OUTPUT_GRAPH_DIR = "output/graphs"

SQLITE_DB = "output/street_history.sqlite"
MERGED_STREET_DATA_TABLE = "street_terms"
TERMS_DICTIONARY_TABLE = "terms_dictionary"
TERMS_LANGUAGE_DICTIONARY_TABLE = "terms_language_dictionary"

MPI_TAGS = enum('READY', 'DONE', 'EXIT', 'START')

PUNCTUATION = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
