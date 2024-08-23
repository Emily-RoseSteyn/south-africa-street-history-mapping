import argparse
import os.path
from datetime import datetime
from time import time
from typing import Any

import geopandas as gpd
import matplotlib.font_manager as font_manager
import osmnx as ox
from geopandas import GeoDataFrame

from mapping.country_colour_map import DEFAULT_BACKGROUND_COLOUR, get_custom_legend, get_colour
from mapping.lookup_origin import map_street_to_origin
from utils.env_variables import OUTPUT_IMAGES_DIR, PUNCTUATION, OUTPUT_GDF_DIR
from utils.logger import get_logger

logger = get_logger()


def get_gdf(address, graph, processed_place_name, label, map_language, use_cache: bool = True):
    logger.info(f"Getting geodataframe for {address}")
    gdf_output_dir = OUTPUT_GDF_DIR
    if not os.path.exists(gdf_output_dir):
        os.makedirs(gdf_output_dir)

    filename = f"{processed_place_name}_{label}_language.parquet" if map_language \
        else f"{processed_place_name}_{label}.parquet"
    gdf_output_path = os.path.join(gdf_output_dir, filename)

    if os.path.isfile(gdf_output_path) and use_cache:
        logger.info(f"Found existing parquet for {address}")
        return gpd.read_parquet(gdf_output_path)

    # Otherwise, convert to geopandas
    gdf = ox.graph_to_gdfs(graph, nodes=False)
    # Map street origins with colours
    gdf = gdf.apply(lambda x: map_street_to_origin(x, map_language), axis=1)

    # Save
    gdf = gpd.GeoDataFrame(gdf[["origin", "name", "primary_term", "likelihood", "geometry"]], index=gdf.index)
    gdf.to_parquet(gdf_output_path)

    logger.info(f"Mapped origins and colours for {address}.")
    logger.info(f"Saved parquet to {gdf_output_path}")
    return gdf

def plot_osmnx_graph(custom_font, edge_linewidth, fig_size, gdf, graph, map_language, processed_place_name, start_time):
    # Get colours
    gdf["colour"] = gdf["origin"].apply(lambda x: get_colour(x))
    logger.info(f"Plotting...")
    # Map coloured streets on graph
    map_fig, map_ax = ox.plot_graph(graph, node_size=0, figsize=fig_size,
                                    dpi=300, bgcolor=DEFAULT_BACKGROUND_COLOUR,
                                    save=False, edge_color=gdf["colour"],
                                    edge_linewidth=edge_linewidth, edge_alpha=1, show=False)
    # Get custom legend
    origins_in_fig = gdf["origin"].unique()
    legend_elements = get_custom_legend(origins_in_fig)
    # Allow custom font to match output if necessary
    font = font_manager.FontProperties(family=custom_font, size=32)
    map_ax.legend(handles=legend_elements, bbox_to_anchor=(1.4, 1),
                  facecolor=DEFAULT_BACKGROUND_COLOUR, framealpha=1, prop=font)
    # Create directory if it doesn't exist
    output_dir = OUTPUT_IMAGES_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Save figure
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f"{timestamp}_{processed_place_name}_language.png" if map_language \
        else f"{timestamp}_{processed_place_name}.png"
    output_path = os.path.join(output_dir, filename)
    map_fig.savefig(output_path, dpi=300, bbox_inches='tight', format="png",
                    facecolor=DEFAULT_BACKGROUND_COLOUR, transparent=False)
    process_time = round(int(time() - start_time) / 60, 2)
    logger.info(
        f"Finished mapping! Time spent in minutes: {process_time}")
    return graph, gdf, map_fig


def map_origin_of_polygon(polygon, address: str, edge_linewidth: int = 2, map_language: bool = False,
                          use_cache: bool = True, fig_size: tuple = (32, 32), custom_font: str = "sans-serif"
                          ) -> tuple[Any, GeoDataFrame, Any]:
    processed_place_name = address.split(',')[0].strip(PUNCTUATION).replace(' ', '_').lower()
    logger.info(f"Mapping origins of {address} by polygon")
    start_time = time()

    # Getting OSMNX graph from address
    graph = ox.graph_from_polygon(polygon, network_type='drive')

    logger.info(f"Retrieved graph for polygon of address {address}")

    # Getting dictionary geodataframe
    # TODO: Prevent overwriting of existing polygon files?
    gdf = get_gdf(address, graph, processed_place_name, 'polygon', map_language, use_cache)

    return plot_osmnx_graph(custom_font, edge_linewidth, fig_size, gdf, graph, map_language, processed_place_name,
                            start_time)




def map_origin_of_address(address: str, dist: int = 1000, edge_linewidth: int = 2, map_language: bool = False,
                          use_cache: bool = True, fig_size: tuple = (32, 32), custom_font: str = "sans-serif"
                          ) -> tuple[Any, GeoDataFrame, Any]:
    processed_place_name = address.split(',')[0].strip(PUNCTUATION).replace(' ', '_').lower()
    logger.info(f"Mapping origins of address {address} within {dist} meters")
    start_time = time()

    # Getting OSMNX graph from address
    graph = ox.graph_from_address(address, network_type='drive', dist=dist)

    logger.info(f"Retrieved graph for address {address}")

    # Getting dictionary geodataframe
    gdf = get_gdf(address, graph, processed_place_name, dist, map_language, use_cache)
    return plot_osmnx_graph(custom_font, edge_linewidth, fig_size, gdf, graph, map_language, processed_place_name,
                            start_time)


def main() -> tuple[Any, Any, Any] | None:
    parser = argparse.ArgumentParser()

    address_key = "address"
    distance_key = "distance"
    line_width_key = "line_width"
    language_key = "language"
    use_cache_key = "use_cache"
    fig_size_key = "fig_size"

    parser.add_argument(f"{address_key}", help="The address around which to plot")
    parser.add_argument(f"--{distance_key}", help="The distance around address to plot", nargs='?', default=1000,
                        type=int)
    parser.add_argument(f"--{line_width_key}", help="The line width to plot", nargs='?', default=2, type=int)
    parser.add_argument(f"--{language_key}", help="Use language mapping instead of dictionary", nargs='?',
                        default=False,
                        type=bool)
    parser.add_argument(f"--{use_cache_key}", help="Use cache when mapping - defaults to True", nargs='?',
                        default=True,
                        type=bool)
    parser.add_argument(f"--{fig_size_key}", help="Figure size for output figure - defaults to 32, assumes a square", nargs='?',
                        default=32,
                        type=int)

    args = vars(parser.parse_args())
    address = args[address_key]
    edge_line_width = args[line_width_key]
    distance = args[distance_key]
    map_language = args[language_key]
    use_cache = args[use_cache_key]
    fig_size = args[fig_size_key]

    print(args)

    return map_origin_of_address(address, distance, edge_line_width, map_language, use_cache, (fig_size, fig_size))


if __name__ == "__main__":
    main()
