from geopandas import GeoDataFrame


def calculate_length_by_origin(dataframe: GeoDataFrame):
    # Assume dataframe has geometry linestring in EPSG:4326
    modified = dataframe.copy()
    # Convert to right CRS for length calculations (best practice)
    modified["geometry"] = modified["geometry"].to_crs(epsg=32735)
    modified["length_km"] = modified["geometry"].length / 1000

    # # Group by origin
    grouped_by_origin = modified[["origin", "length_km"]].groupby("origin").sum()
    total_length = grouped_by_origin["length_km"].sum()
    grouped_by_origin["%"] = grouped_by_origin["length_km"]/total_length * 100
    grouped_by_origin = grouped_by_origin.sort_values(by="%", ascending=False)
    return grouped_by_origin.reset_index()
