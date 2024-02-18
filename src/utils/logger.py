import logging

from utils.env_variables import LOGGING_LEVEL


def get_logger() -> logging.Logger:
    logging.basicConfig(level=LOGGING_LEVEL)
    return logging.getLogger("masters")
