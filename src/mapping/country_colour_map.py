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
        "south_africa": "#e5c494",
        "belgium": "#ffd000",
        "england": "#66c2a5",
        "france": "#ffa886",
        "germany": "#cd212a",
        "ireland": "#b3f469",
        "italy": "#e78ac3",
        "netherlands": "#ff9325",
        "northern_ireland": "#009a61",
        "portugal": "#ffec4f",
        "scotland": "#91a4ff",
        "spain": "#800080",
        "wales": "#ccebc5",
        "afrikaans": "#a65628",
        "dutch": "#ff9325",
        "english": "#66c2a5",
        "french": "#ffa886",
        "german": "#cd212a",
        "italian": "#e78ac3",
        "portuguese": "#ffec4f",
        "sotho": "#a6761d",
        "spanish": "#800080",
        "xhosa": "#d95f02",
        "zulu": "#f781bf",
    }


DEFAULT_COLOUR = "#d9d9d9"
DEFAULT_BACKGROUND_COLOUR = "#ffffff"
COLOUR_MAP = country_colour_map_static()


def get_colour(origin):
    return COLOUR_MAP.get(origin, DEFAULT_COLOUR)


def get_custom_legend(figure_origins: pd.DataFrame):
    legend_elements = []
    for origin in COLOUR_MAP:
        if origin in figure_origins:
            legend_elements.append(
                Patch(facecolor=COLOUR_MAP[origin], label=str(origin).replace('_', ' ').title()))
    legend_elements.append(Patch(facecolor=DEFAULT_COLOUR, label="None"))
    return legend_elements
