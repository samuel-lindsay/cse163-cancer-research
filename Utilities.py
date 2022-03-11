import pandas as pd
import geopandas as gpd
# from utilities_helper import strip_county_name

class Utils:
    def get_mir(data, on, rate_col):
        """
        Takes in the already cleaned data. Given a set of columns to merge
        on, and desired col. it splits the data into mortality and
        incidence rows, then merges together based on the keys. Then it
        calculates an MIR and appends it to the data set with a new column.
        Returns the data with the MIR.
        """
        data = data.astype({rate_col: 'float32'})
        mortality = data[data["EVENT_TYPE"] == "Mortality"]
        incidence = data[data["EVENT_TYPE"] == "Incidence"]
        joined = pd.merge(mortality, incidence, how='inner', on=on)
        joined["MIR"] = joined[rate_col + "_x"] / joined[rate_col + "_y"]
        return joined


    def remove_rows(data, chars):
        """
        Filters rows based on a set of characters.
        Used to clean out the 4 characters that are all used to represent
        a NA value.
        """
        filter = data != chars[0]  # get base filter
        for c in chars:
            filter = filter & (data != c)

        return data[filter.all(1)]


    def _strip_county_name(area):
        """
        This method is a helper to function clean_join_shp.
        It takes a single entry from the by_county DataFrame and
        cleans the entry to match the format in counties GeoDataFrame.
        """
        elements = area.split(":")
        county = elements[0] +" " + elements[1].split("(")[0].strip()
        return county


    def clean_join_shp(by_county, counties):
        """
        Takes a Dataframe by_county and a GeoDataFrame counties as input.
        Returns a new GeoDataFrame prepared_shp. This function joins the
        rows from two dataset on their county names for further plotting
        operations.
        """
        helper = "_strip_county_name"
        by_county.loc[:, "county"] = by_county.loc[:, "AREA"].apply(helper)
        counties.loc[:, "county"] = counties.loc[:, "STUSPS"] + \
                                    " " + counties.loc[:, "NAMELSAD"]
        by_county_c = by_county.astype({"county": "str"}, copy=True)
        counties_c = counties.astype({"county": "str"}, copy=True)
        prepared_shp = counties_c.merge(by_county_c, left_on="county",
                                        right_on="county", how="left")
        return prepared_shp