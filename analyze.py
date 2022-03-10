import pandas as pd
from utilities import Utils

AGE_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAGE.TXT"
AREA_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA.TXT"
COUNTY_DATA_PATH = "data\\USCS-1999-2018-ASCII\\BYAREA_COUNTY.TXT"

def state_change(data):
    data = data[['AREA', 'AGE_ADJUSTED_RATE', 'EVENT_TYPE', 'RACE', 'SEX', 'SITE', 'YEAR']]
    data = data[(data["SITE"] == "All Cancer Sites Combined") & (data["SEX"] == "Male and Female")]
    data = Utils.removeRows(data, ['~', '+', '.', '-'])
    data = Utils.getmir(data, ['AREA', 'RACE', 'SEX', 'SITE', 'YEAR'],
                        'AGE_ADJUSTED_RATE')
    data = data[["AREA", "YEAR", "MIR"]]
    grouped = data.groupby(by="AREA")
    state_change = grouped['MIR'].first() - grouped['MIR'].last()
    return state_change


def main():
    byage = pd.read_csv(AGE_DATA_PATH, sep="|", low_memory=False)
    byarea = pd.read_csv(AREA_DATA_PATH, sep="|", low_memory=False)
    bycounty = pd.read_csv(COUNTY_DATA_PATH, sep="|", low_memory=False)
    change = state_change(byarea)
    print("Best Improvement: " + str(change.idxmax()) + " " + str(change.max()))
    print("Worse improvement: " + str(change.idxmin()) + " " + str(change.min()))


if __name__ == "__main__":
    main()
