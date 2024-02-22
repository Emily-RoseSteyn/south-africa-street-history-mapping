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
        COUNTRY_ISO_CODE_NAME_MAP["ZA"]: "#e5c494",
        COUNTRY_ISO_CODE_NAME_MAP["BE"]: "#ffd000",
        COUNTRY_ISO_CODE_NAME_MAP["GB-ENG"]: "#66c2a5",
        COUNTRY_ISO_CODE_NAME_MAP["FR"]: "#ffa886",
        COUNTRY_ISO_CODE_NAME_MAP["DE"]: "#cd212a",
        COUNTRY_ISO_CODE_NAME_MAP["IE"]: "#b3f469",
        COUNTRY_ISO_CODE_NAME_MAP["IT"]: "#e78ac3",
        COUNTRY_ISO_CODE_NAME_MAP["NL"]: "#ff9325",
        COUNTRY_ISO_CODE_NAME_MAP["GB-NIR"]: "#009a61",
        COUNTRY_ISO_CODE_NAME_MAP["PT"]: "#ffec4f",
        COUNTRY_ISO_CODE_NAME_MAP["GB-SCT"]: "#91a4ff",
        COUNTRY_ISO_CODE_NAME_MAP["ES"]: "#800080",
        COUNTRY_ISO_CODE_NAME_MAP["GB-WLS"]: "#ccebc5",
        "afrikaans": "#a65628",
        "english": "#66c2a5",
        "sotho": "#a6761d",
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
