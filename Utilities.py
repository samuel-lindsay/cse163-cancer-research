import pandas as pd
import geopandas as gpd
import altair as alt


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
        check = data != chars[0]
        for c in chars:
            check = check & (data != c)
        return data[check.all(1)]

    def _strip_geoid(area):
        """
        This method is a helper to function clean_join_shp.
        It takes a single entry from the by_county DataFrame and
        cleans the entry to match the format in counties GeoDataFrame.
        """
        geoid = area[area.index("(") + 1: area.index(")")].strip()
        return geoid

    def _clean_join_shp(by_county, counties):
        """
        Takes a Dataframe by_county and a GeoDataFrame counties as input.
        Returns a new GeoDataFrame prepared_shp. This function joins the
        rows from two dataset on their county names for further plotting
        operations.
        """
        # states_for_by_county = (by_county["STATE_x"] != "AK") & \
        #                        (by_county["STATE_x"] != "HI")
        # states_for_counties = (counties["STUSPS"] != "AK") & \
        #                       (counties["STUSPS"] != "HI")
        # by_county = by_county[states_for_by_county]
        # counties = counties[states_for_counties]

        by_county.loc[:, "geoid"] = by_county.loc[:, "AREA"] \
                                             .apply(Utils._strip_geoid)
        by_county = by_county.astype({"geoid": "float32"})
        counties = counties.astype({"GEOID": "float32"})
        prepared_shp = counties.merge(by_county, left_on="GEOID",
                                      right_on="geoid", how="left")
        states_shp = counties[["STUSPS", "geometry"]]
        states_shp = states_shp.dissolve(by="STUSPS")

        return prepared_shp, states_shp

    def generate_map(by_county, counties):
        """
        Takes a Dataframe by_county and a GeoDataFrame counties as input.
        This function will use by_county and counties to create an
        interactive map of MIR among all cancer types in the US. The map
        is responsive to selecting different race.
        """
        races = [str(race) for race in by_county["RACE"].unique()]
        prepared_shp, states_shp = Utils._clean_join_shp(by_county, counties)

        # races = prepared_shp["RACE"] == "All Races"
        # sites = prepared_shp["SITE"] == "All Cancer Sites Combined"
        # sexes = prepared_shp["SEX"] == "Male and Female"
        # prepared_shp = prepared_shp[races & sites & sexes]

        alt.data_transformers.disable_max_rows()
        scale = alt.Scale(domain=[0.10, 1.12])

        background = alt.Chart(states_shp) \
                        .mark_geoshape(fill="lightgray", stroke="white")

        race_dropdown = alt.binding_select(options=races, name="Race")
        race_select = alt.selection_single(bind=race_dropdown,
                                           fields=["Race", "geometry"])

        mir_highlight = alt.Chart(prepared_shp) \
           .mark_geoshape() \
           .encode(color = alt.Color("MIR:Q", scale=scale)) \
           .add_selection(race_select) \
           .transform_filter(race_select) \
           .properties(title="Mortality Incidence Rate for US counties (2014-2018)")


        # filter_races = mir_highlight.add_selection(race_select) \
        #                             .transform_filter(race_select) \
        #                             .properties(title="Race Filtering")

        # (background + mir_highlight).save("alt_test.html")
        (background + mir_highlight).save("interactive_test.html")
