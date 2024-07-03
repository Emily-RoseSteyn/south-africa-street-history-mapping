import argparse
from typing import Any

import osmnx

from mapping.calculate_length_by_origin import calculate_length_by_origin
from mapping.main import map_origin_of_address


def process(address, distance, edge_line_width, use_cache, fig_size):
    print("-------------------------------------DICTIONARY-------------------------------------")
    graph, gdf, map_fig = map_origin_of_address(address, distance, edge_linewidth=edge_line_width, use_cache=use_cache,
                                                custom_font="Poppins", fig_size=fig_size)
    print("-------------------------------------LANGUAGE-------------------------------------")
    map_origin_of_address(address, distance, edge_linewidth=edge_line_width, map_language=True, use_cache=use_cache,
                          custom_font="Poppins", fig_size=fig_size)

    print("-------------------------------------BOUNDING BOX-------------------------------------")
    point = osmnx.geocode(address)
    bounding_box = osmnx.utils_geo.bbox_from_point(point, dist=distance)
    print(bounding_box)

    print("-------------------------------------CALCULATE LENGTHS-------------------------------------")
    grouped_by_origin = calculate_length_by_origin(gdf)
    print(grouped_by_origin)
    return grouped_by_origin


def map_e2e() -> tuple[Any, Any, Any] | None:
    print("-------------------------------------PROCESSING ADDRESS-------------------------------------")
    parser = argparse.ArgumentParser()

    address_key = "address"
    distance_key = "distance"
    line_width_key = "line_width"
    use_cache_key = "use_cache"
    fig_size_key = "fig_size"

    parser.add_argument(f"{address_key}", help="The address around which to plot")
    parser.add_argument(f"--{distance_key}", help="The distance around address to plot", nargs='?', default=1000,
                        type=int)
    parser.add_argument(f"--{line_width_key}", help="The line width to plot", nargs='?', default=2, type=int)

    parser.add_argument(f"--{use_cache_key}", help="Use cache when mapping - defaults to True", nargs='?',
                        default=True,
                        type=bool)
    parser.add_argument(f"--{fig_size_key}", help="Figure size for output figure - defaults to 32, assumes a square",
                        nargs='?',
                        default=32,
                        type=int)

    args = vars(parser.parse_args())
    address = args[address_key]
    edge_line_width = args[line_width_key]
    distance = args[distance_key]
    use_cache = args[use_cache_key]
    fig_size = args[fig_size_key]

    print(args)

    return process(address, distance, edge_line_width, use_cache, (fig_size, fig_size))


if __name__ == "__main__":
    map_e2e()
