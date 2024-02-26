import sqlite3

import osmnx as ox
import pandas as pd
from matplotlib.patches import Patch
from mizani.colors.brewer.qualitative import Set2

from utils.country_iso_map import COUNTRY_ISO_CODE_NAME_MAP
from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE

conn = sqlite3.connect(SQLITE_DB)

ORIGIN_CMAP = Set2.name


def country_colour_map_dynamic():
    countries = pd.read_sql_query(
        f"SELECT country FROM {MERGED_STREET_DATA_TABLE} "
        f"GROUP BY country ",
        conn)
    edge_types = countries["country"].value_counts()
    color_list = ox.plot.get_colors(n=len(edge_types), alpha=None, cmap=ORIGIN_CMAP)
    return pd.Series(color_list, index=edge_types.index).to_dict()


def country_colour_map_static():
    return {
        # Countries
        "south_africa": "#f8d095",
        "england": "#2fc495",
        "ireland": "#afee48",
        "northern_ireland": "#afee48",
        "scotland": "#afee48",
        "wales": "#afee48",
        "france": "#9bb2e7",
        "germany": "#ffd518",
        "belgium": "#ff7d4a",
        "netherlands": "#ff7d4a",
        "italy": "#f286c8",
        "portugal": "#f286c8",
        "spain": "#f286c8",
        # Languages
        "afrikaans": "#a65628",
        "xhosa": "#3ca53c",
        "zulu": "#3ca53c",
        "sotho": "#84ff84",
        "dutch": "#ff7d4a",
        "english": "#2fc495",
        "french": "#9bb2e7",
        "german": "#ffd518",
        "italian": "#f286c8",
        "portuguese": "#f286c8",
        "spanish": "#f286c8",
    }


DEFAULT_COLOUR = "#d9d9d9"
DEFAULT_BACKGROUND_COLOUR = "#ffffff"
COLOUR_MAP = country_colour_map_static()


def get_colour(origin):
    return COLOUR_MAP.get(origin, DEFAULT_COLOUR)


LEGEND_LABEL_MAP = {
    "south_africa": "South Africa",
    "england": "England",
    "ireland": "Ireland, Northern Ireland,\nScotland, Wales",
    "northern_ireland": "Ireland, Northern Ireland,\nScotland, Wales",
    "scotland": "Ireland, Northern Ireland,\nScotland, Wales",
    "wales": "Ireland, Northern Ireland,\nScotland, Wales",
    "france": "France",
    "germany": "Germany",
    "belgium": "Netherlands, Belgium",
    "netherlands": "Netherlands, Belgium",
    "italy": "Portugal, Spain, Italy",
    "portugal": "Portugal, Spain, Italy",
    "spain": "Portugal, Spain, Italy",
    "afrikaans": "Afrikaans",
    "dutch": "Dutch",
    "english": "English",
    "french": "French",
    "german": "German",
    "italian": "Portuguese, Spanish, Italian",
    "portuguese": "Portuguese, Spanish, Italian",
    "sotho": "Sesotho",
    "spanish": "Portuguese, Spanish, Italian",
    "xhosa": "Xhosa/Zulu (Nguni)",
    "zulu": "Xhosa/Zulu (Nguni)",
}


def get_custom_legend(figure_origins: pd.DataFrame):
    legend_dictionary = {}
    for origin in COLOUR_MAP:
        if origin in figure_origins:
            legend_dictionary[LEGEND_LABEL_MAP[origin]] = COLOUR_MAP[origin]

    legend_elements = []
    for label in legend_dictionary:
        legend_elements.append(
            Patch(facecolor=legend_dictionary[label], label=label))
    legend_elements.append(Patch(facecolor=DEFAULT_COLOUR, label="None/Unknown"))
    return legend_elements
