import os.path
import sys
from datetime import datetime
from time import time

import geopandas as gpd
import osmnx as ox

from mapping.country_colour_map import DEFAULT_BACKGROUND_COLOUR, get_custom_legend
from mapping.lookup_origin import map_street_to_origin
from utils.env_variables import OUTPUT_IMAGES_DIR, PUNCTUATION, OUTPUT_GDF_DIR
from utils.logger import get_logger

logger = get_logger()


def get_gdf(address, graph, processed_place_name):
    gdf_output_dir = OUTPUT_GDF_DIR
    if not os.path.exists(gdf_output_dir):
        os.makedirs(gdf_output_dir)
    gdf_output_path = os.path.join(gdf_output_dir, f"{processed_place_name}.geojson")

    if os.path.isfile(gdf_output_path):
        return gpd.read_file(gdf_output_path)

    # Otherwise, convert to geopandas
    gdf = ox.graph_to_gdfs(graph, nodes=False)
    logger.info(f"Converted to geopandas for address {address}")
    # Map street origins with colours
    gdf = gdf.apply(lambda x: map_street_to_origin(x), axis=1)

    # gdf_output_dir = OUTPUT_GDF_DIR
    # if not os.path.exists(gdf_output_dir):
    #     os.makedirs(gdf_output_dir)
    # gdf_output_path = os.path.join(gdf_output_dir, f"{processed_place_name}.geojson")

    # Save
    # TODO: OSMNX format prevents saving in geojson easily
    # gdf.to_file(gdf_output_path, driver="GeoJSON")
    # logger.info(f"Saved to {gdf_output_path}")
    logger.info(f"Mapped origins and colours for {address}.")
    return gdf


def map_origin_of_address(address: str, dist: int = 1000, edge_linewidth: int = 2) -> None:
    processed_place_name = address.split(',')[0].strip(PUNCTUATION).replace(' ', '_').lower()
    logger.info(f"Mapping origins of address {address} within {dist} meters")
    start_time = time()

    # Getting OSMNX graph from address
    graph = ox.graph_from_address(address, network_type='drive', dist=dist)

    logger.info(f"Retrieved graph for address {address}")

    # Getting geodataframe with colours
    gdf = get_gdf(address, graph, processed_place_name)

    logger.info(f"Plotting...")
    # Map coloured streets on graph
    map_fig, map_ax = ox.plot_graph(graph, node_size=0,
                                    dpi=100, bgcolor=DEFAULT_BACKGROUND_COLOUR,
                                    save=False, edge_color=gdf["colour"],
                                    edge_linewidth=edge_linewidth, edge_alpha=1, show=False)

    # Get custom legend
    kensington_origins_in_fig = gdf["origin"].unique()
    kensington_legend_elements = get_custom_legend(kensington_origins_in_fig)
    map_ax.legend(handles=kensington_legend_elements, bbox_to_anchor=(1.4, 1), fontsize=8,
                  facecolor=DEFAULT_BACKGROUND_COLOUR, framealpha=1)

    # Create directory if it doesn't exist
    output_dir = OUTPUT_IMAGES_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save figure
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    output_path = os.path.join(output_dir, f"{timestamp}_{processed_place_name}.png")
    map_fig.savefig(output_path, dpi=300, bbox_inches='tight', format="png",
                    facecolor=DEFAULT_BACKGROUND_COLOUR, transparent=False)

    process_time = round(int(time() - start_time) / 60, 2)

    logger.info(
        f"Finished mapping! Time spent in minutes: {process_time}")


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Please provide an address to map")
        return None

    address = sys.argv[1]

    distance = 1000
    if len(sys.argv) > 2:
        try:
            distance = int(sys.argv[2])
        except ValueError:
            logger.error(f"Distance not an integer. Carrying on with distance = {distance}")

    edge_line_width = 2
    if len(sys.argv) > 3:
        try:
            edge_line_width = int(sys.argv[3])
        except ValueError:
            logger.error(f"Edge line width is not an integer. Carrying on with distance = {edge_line_width}")

    map_origin_of_address(address, distance, edge_line_width)


if __name__ == "__main__":
    main()
