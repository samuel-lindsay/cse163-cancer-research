"""
Sam Lindsay and Peter Xu
CSE 163
Top level program that is used to analyze the cancer data set. Loads the data,
cleans it, then creates visualizations.
"""


import pandas as pd
import geopandas as gpd
from utilities import Utils
from plots import CancerPlots


AREA_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA.TXT"
SITE_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYSITE.TXT"
COUNTY_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA_COUNTY.TXT"
SHP_DATA_PATH = "data\\2020_us_county_shp\\cb_2020_us_county_20m.shp"


def state_change(data):
    """
    Takes in a DataFrame data and returns a list of MIR percent changes between
    1999 and 2018 for each state. Also creates a plot showing the MIR for each
    state over time and saves it to "state_improvement_plot.html".
    Only considers data for all races, sexes, and types of cancer combined in
    order to best compare different states.
    """
    data = Utils.filter_sex_site_race(data)
    data = data[['AREA', 'AGE_ADJUSTED_RATE', 'EVENT_TYPE', 'YEAR']]
    data = Utils.remove_rows(data=data, chars=['~', '+', '.', '-'])
    data = Utils.get_mir(data=data,
                         on=['AREA', 'YEAR'],
                         rate_col='AGE_ADJUSTED_RATE')
    data = data[["AREA", "YEAR", "MIR"]]
    data = data.sort_values(["YEAR"])
    CancerPlots.make_state_plot(data)
    grouped = data.groupby(by="AREA")
    state_change = (grouped['MIR'].last() - grouped['MIR'].first()) \
        / grouped['MIR'].first()
    return state_change


def cancer_change(data):
    """
    This function takes in a DataFrame data and returns a list of MIR
    percentage change between 1999 and 2018 for each type of cancer.
    Also creates a plot showing the MIR of all types of cancer over the
    time period and saves it to "cancer_type_plot.html".
    Here, we only consider the data for all races and all sexes combined
    as they cover the most portion of population in our dataset.
    """
    data = Utils.filter_sex_site_race(data, site=None)
    data = Utils.remove_rows(data=data, chars=['~', '+', '.', '-'])
    data = data[['SITE', 'AGE_ADJUSTED_RATE', 'EVENT_TYPE', 'YEAR']]
    data = Utils.get_mir(data=data,
                         on=['SITE', 'YEAR'],
                         rate_col='AGE_ADJUSTED_RATE')
    data = data[["YEAR", "MIR", "SITE"]]
    data = data.sort_values(["YEAR"])
    CancerPlots.make_cancer_plot(data)
    grouped = data.groupby(by="SITE")
    cancer_change = (grouped['MIR'].last() - grouped['MIR'].first()) \
        / grouped['MIR'].first()
    return cancer_change


def create_interactive(by_county, counties):
    """
    Takes in two data sets: "by_county" is a DataFrame containing cancer data
    that is broken down by county and "counties" is geospatial data defining
    the shape of each county. Does not return anything, but it does create
    an interactive visualization showing the MIR in each county filtered by
    race. This visualization is saved to "state_race_map.html".
    """
    by_county = Utils.filter_alaska_hawaii(by_county, "STATE")
    counties = Utils.filter_alaska_hawaii(counties, "STUSPS")

    by_county_c = by_county[["AREA", "RACE", "SITE", "YEAR", "EVENT_TYPE",
                             "AGE_ADJUSTED_RATE", "SEX", "STATE"]].copy()
    by_county_c = Utils.filter_sex_site_race(by_county, race=None)
    counties_c = counties[["GEOID", "NAMELSAD", "STUSPS", "STATE_NAME",
                           "geometry"]].copy()

    by_county_c = Utils.remove_rows(data=by_county_c,
                                    chars=['+', '~', '.', '-'])
    by_county_c = Utils.get_mir(data=by_county_c,
                                on=['AREA', 'RACE', 'SEX', 'SITE', 'YEAR'],
                                rate_col='AGE_ADJUSTED_RATE')
    CancerPlots.generate_map(by_county_c, counties_c)


def main():
    by_area = pd.read_csv(AREA_DATA_PATH, sep="|", low_memory=False)
    by_site = pd.read_csv(SITE_DATA_PATH, sep="|", low_memory=False)
    by_county = pd.read_csv(COUNTY_DATA_PATH, sep="|", low_memory=False)
    counties = gpd.read_file(SHP_DATA_PATH)

    # Question 1 - Which state had the greatest change?
    change_by_state = state_change(by_area)
    print("Greatest change_by_state in MIR: " + str(change_by_state.idxmax()) +
          " " + str(change_by_state.max()))
    print("Smallest change_by_state in MIR: " + str(change_by_state.idxmin()) +
          " " + str(change_by_state.min()))

    # Question 2 - Which type of cancer had the greatest change?
    change_by_cancer = cancer_change(by_site)
    print("Greatest change_by_cancer in MIR: "
          + str(change_by_cancer.idxmax()) + " " + str(change_by_cancer.max()))
    print("Smallest change_by_cancer in MIR: "
          + str(change_by_cancer.idxmin()) + " " + str(change_by_cancer.min()))

    # Question 3 - In the same county, what is the difference in racial groups?
    create_interactive(by_county, counties)


if __name__ == "__main__":
    main()
