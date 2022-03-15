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
    """
    data = Utils.filter_sex_site(data)
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
    percentage change between 2018 and 1999 for each type of cancer.
    Here, we only consider the data for all races and all sexes combined
    as they cover the most portion of population in our dataset.
    """
    data = Utils.filter_sex_site(data)
    data = data[['SITE', 'AGE_ADJUSTED_RATE', 'EVENT_TYPE', 'YEAR']]
    data = Utils.remove_rows(data=data, chars=['~', '+', '.', '-'])
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
    by_county = Utils.filter_alaska_hawaii(by_county, "STATE")
    counties = Utils.filter_alaska_hawaii(counties, "STUSPS")
    by_county_c = Utils.filter_sex_site(by_county)

    by_county_c = by_county[["AREA", "RACE", "SITE", "YEAR", "EVENT_TYPE",
                             "AGE_ADJUSTED_RATE", "SEX", "STATE"]].copy()
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

    change_by_state = state_change(by_area)
    print("Greatest change_by_state in MIR: " + str(change_by_state.idxmax()) +
          " " + str(change_by_state.max()))
    print("Smallest change_by_state in MIR: " + str(change_by_state.idxmin()) +
          " " + str(change_by_state.min()))

    change_by_cancer = cancer_change(by_site)
    print("Greatest change_by_cancer in MIR: "
          + str(change_by_cancer.idxmax()) + " " + str(change_by_cancer.max()))
    print("Smallest change_by_cancer in MIR: "
          + str(change_by_cancer.idxmin()) + " " + str(change_by_cancer.min()))

    create_interactive(by_county, counties)


if __name__ == "__main__":
    main()
