# env_variables.py

"""This module defines project-level env variable keys."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

WORD_LENGTH_THRESHOLD = 3

STREET_DATA_DIR = "data/streets"
PROCESSED_STREET_DATA_DIR = "output/streets"

STREET_OUTPUT_PREFIX = "processed"
