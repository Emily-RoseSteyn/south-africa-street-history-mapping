import logging
import warnings

from utils.env_variables import LOGGING_LEVEL

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_logger() -> logging.Logger:
    logging.basicConfig(level=LOGGING_LEVEL)
    return logging.getLogger("_")
