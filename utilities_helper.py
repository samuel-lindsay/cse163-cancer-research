def strip_county_name(area):
    """
    This method is a helper to function clean_join_shp.
    It takes a single entry from the by_county DataFrame and
    cleans the entry to match the format in counties GeoDataFrame.
    """
    elements = area.split(":")
    county = elements[0] +" " + elements[1].split("(")[0].strip()
    return county