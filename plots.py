"""
Sam Lindsay and Peter Xu
CSE 163
This file contains the definition for CancerPlots, the class which contains all
of the functions related to creating altair visualizations for the data.
"""
import altair as alt


class CancerPlots:
    """
    CancerPlots is responsible for creating the altair visualizations for
    the cancer data.
    """

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
        by_county.loc[:, "geoid"] = by_county.loc[:, "AREA"] \
                                             .apply(CancerPlots._strip_geoid)
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
        prepared_shp, states_shp = CancerPlots._clean_join_shp(by_county,
                                                               counties)

        alt.data_transformers.disable_max_rows()
        scale = alt.Scale(domain=[0.10, 1.12])

        race_dropdown = alt.binding_select(options=races)
        race_select = alt.selection_single(fields=["RACE"],
                                           bind=race_dropdown, name="Race",
                                           init={"RACE": races[0]})

        background = alt.Chart(states_shp) \
                        .mark_geoshape(fill="lightgray", stroke="white")

        mir_highlight = alt.Chart(prepared_shp).mark_geoshape().encode(
            color=alt.Color("MIR:Q", scale=scale)
        ).add_selection(
            race_select
        ).transform_filter(
            race_select
        ).properties(
            title="Cancer MIR per County from 2014-2018 by Race"
        )

        (background + mir_highlight).save("state_race_map.html")

    def make_state_plot(data):
        """
        Takes in state-level data that has already been cleaned, filtered,
        and given an MIR column. Then creates an interactive altair line
        chart out of the changes in MIR among all 50 states and DC from
        1999 to 2018.
        """
        data = data[data["YEAR"] != "2014-2018"]
        data = data.sort_values(['YEAR'])
        states = data["AREA"].unique()
        states.sort()
        state_dropdown = alt.binding_select(options=states)
        state_select = alt.selection_single(fields=['AREA'],
                                            bind=state_dropdown, name="State")
        background_chart = alt.Chart(data).mark_line().encode(
            x='YEAR',
            y=alt.Y('MIR', scale=alt.Scale(domain=[0.275, 0.55])),
            detail="AREA",
            tooltip="AREA",
            color=alt.value("lightgray")
        )
        selected_state = alt.Chart(data).mark_line().encode(
            x='YEAR',
            y=alt.Y('MIR', scale=alt.Scale(domain=[0.275, 0.55])),
            detail="AREA",
            tooltip="AREA",
            color="AREA"
        ).add_selection(
            state_select
        ).transform_filter(
            state_select
        ).properties(
            title="State MIR from 1999-2018"
        )
        (background_chart + selected_state).save("state_improvement_plot.html")

    def make_cancer_plot(data):
        """
        Takes in a DataFrame data which is cleaned, filtered, given
        an MIR column, and grouped by cancer types. Then creates an
        interactive altair line chart out of the changes in MIR among
        all kinds of cancers from 1999 to 2018.
        """
        data = data[data["YEAR"] != "2014-2018"]
        data = data.sort_values(["YEAR"])
        cancers = data["SITE"].unique()
        cancers.sort()
        cancer_dropdown = alt.binding_select(options=cancers)
        cancer_select = alt.selection_single(fields=["SITE"],
                                             bind=cancer_dropdown,
                                             name="Cancer Type")
        background_chart = alt.Chart(data).mark_line().encode(
            x="YEAR",
            y="MIR",
            detail="SITE",
            tooltip="SITE",
            color=alt.value("lightgray")
        )
        selected_cancer = alt.Chart(data).mark_line().encode(
            x="YEAR",
            y=alt.Y("MIR", scale=alt.Scale(domain=[0.0, 3.3])),
            detail="SITE",
            tooltip="SITE",
            color="SITE"
        ).add_selection(
            cancer_select
        ).transform_filter(
            cancer_select
        ).properties(
            title="Cancer Type MIRs from 1999-2018"
        )
        (background_chart + selected_cancer).save("cancer_type_plot.html")
