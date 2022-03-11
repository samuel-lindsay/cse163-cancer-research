import pandas as pd
import geopandas as gpd
from utilities import Utils
# from utilities import get_mir, remove_rows, clean_join_shp

AREA_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA.TXT"
COUNTY_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA_COUNTY.TXT"
SHP_DATA_PATH = "data\\2020_us_county_shp\\cb_2020_us_county_20m.shp"



def state_change(data):
    data = data[['AREA', 'AGE_ADJUSTED_RATE', 'EVENT_TYPE',
                 'RACE', 'SEX', 'SITE', 'YEAR']]
    data = data[(data["SITE"] == "All Cancer Sites Combined") &
                (data["SEX"] == "Male and Female")]
    data = Utils.remove_rows(data=data, chars=['~', '+', '.', '-'])
    data = Utils.get_mir(data=data,
                         on=['AREA', 'RACE', 'SEX', 'SITE', 'YEAR'],
                         rate_col='AGE_ADJUSTED_RATE')
    data = data[["AREA", "YEAR", "MIR"]]
    grouped = data.groupby(by="AREA")
    state_change = (grouped['MIR'].last() - grouped['MIR'].first()) / grouped['MIR'].last()
    return state_change


def prepare_shp(by_county, counties):
    by_county = Utils.remove_rows(data=by_county, chars=['~', '.', '-'])
    by_county = Utils.get_mir(data=by_county, 
                              on=['AREA', 'RACE', 'SEX', 'SITE', 'YEAR'],
                              rate_col='AGE_ADJUSTED_RATE')
    prepared_shp = Utils.clean_join_shp(by_county=by_county, counties=counties)
    return prepared_shp


def main():
    by_area = pd.read_csv(AREA_DATA_PATH, sep="|", low_memory=False)
    by_county = pd.read_csv(COUNTY_DATA_PATH, sep="|", low_memory=False)
    counties = gpd.read_file(SHP_DATA_PATH)
    change = state_change(by_area)

    print("Greatest change in MIR: " + str(change.idxmax()) +
          " " + str(change.max()))
    print("Smallest change in MIR: " + str(change.idxmin()) +
          " " + str(change.min()))

    prepared_shp = prepare_shp(by_county, counties)
    no_ak = prepared_shp["STUSPS"] != "AK"
    no_hi = prepared_shp["STUSPS"] != "HI"
    all_races = prepared_shp["RACE"] == "All Races"
    all_cancer_sites = prepared_shp["SITE"] == "All Cancer Sites Combined"
    both_sexes = prepared_shp["SEX"] == "Female"    
    mortality = prepared_shp["EVENT_TYPE"] == "Mortality"
    test_plot = prepared_shp[all_races & all_cancer_sites & both_sexes & mortality & no_ak & no_hi]
    test_plot.plot(figsize=(250, 500))


if __name__ == "__main__":
    main()
