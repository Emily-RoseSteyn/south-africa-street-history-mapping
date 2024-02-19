import os

from utils.env_variables import STREET_DATA_DIR


def get_country_street_files() -> list:
    # Get images directory
    directory = STREET_DATA_DIR
    file_list = []
    for file in os.listdir(directory):
        file_list.append(os.path.join(directory, file))
    return file_list

