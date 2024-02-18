# env_variables.py

"""This module defines project-level env variable keys."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

STREET_DATA_DIR = "data/streets"
