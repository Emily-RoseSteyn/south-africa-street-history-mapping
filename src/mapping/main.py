import os.path
import sys
from pathlib import Path

import osmnx as ox

from mapping.country_colour_map import get_colour, DEFAULT_BACKGROUND_COLOUR, get_custom_legend
from mapping.lookup_origin import map_street_to_origin
from utils.env_variables import OUTPUT_IMAGES_DIR, PUNCTUATION
from utils.logger import get_logger

logger = get_logger()


def map_origin_of_address(address: str) -> None:
    logger.info(f"Mapping origins of address {address}")

    # Getting OSMNX graph from address
    graph = ox.graph_from_address(address, network_type='drive')

    # Convert to geopandas
    gdf = ox.graph_to_gdfs(graph, nodes=False)

    # Map street origins with colours
    gdf = gdf.apply(lambda x: map_street_to_origin(x), axis=1)

    # Map coloured streets on graph
    map_fig, map_ax = ox.plot_graph(graph, node_size=0,
                                    dpi=100, bgcolor=DEFAULT_BACKGROUND_COLOUR,
                                    save=False, edge_color=gdf["colour"],
                                    edge_linewidth=2, edge_alpha=1, show=False)

    # Get custom legend
    kensington_origins_in_fig = gdf["origin"].unique()
    kensington_legend_elements = get_custom_legend(kensington_origins_in_fig)
    map_ax.legend(handles=kensington_legend_elements, bbox_to_anchor=(1.2, 1), fontsize=8,
                           facecolor=DEFAULT_BACKGROUND_COLOUR, framealpha=1)

    # Save figure
    filename = address.split(',')[0].strip(PUNCTUATION).replace(' ', '_')
    output_path = os.path.join(OUTPUT_IMAGES_DIR, f"{filename}.png")
    map_fig.savefig(output_path, dpi=300, bbox_inches='tight', format="png",
                    facecolor=DEFAULT_BACKGROUND_COLOUR, transparent=False)


def main() -> None:
    if len(sys.argv) < 2:
        logger.error("Please provide an address to map")
        return None

    address = sys.argv[1]

    map_origin_of_address(address)


if __name__ == "__main__":
    main()
