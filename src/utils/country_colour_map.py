import sqlite3

import osmnx as ox
import pandas as pd
from matplotlib import colors
from mizani.colors.brewer.qualitative import Set3

from utils.env_variables import SQLITE_DB, MERGED_STREET_DATA_TABLE

conn = sqlite3.connect(SQLITE_DB)


def country_colour_map():
    countries = pd.read_sql_query(
        f"SELECT country FROM {MERGED_STREET_DATA_TABLE} "
        f"GROUP BY country ",
        conn)
    edge_types = countries["country"].value_counts()
    color_list = ox.plot.get_colors(n=len(edge_types), alpha=None, cmap=Set3.name)
    return pd.Series(color_list, index=edge_types.index).to_dict()


DEFAULT_COLOUR = colors.hex2color("#acb0be")
