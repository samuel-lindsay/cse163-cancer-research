# CSE 163 final

## How to run this project

1. Download the required data sets:
    - From [https://www.cdc.gov/cancer/uscs/dataviz/download_data.htm](https://www.cdc.gov/cancer/uscs/dataviz/download_data.htm) select 1999-2018 data set. This should be at the top of the list.
    - From [https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html) select the "Counties" shape file marked 1:20,000,000 scale. This is a little over halfway down the page and should be marked as < 1.0 MB.
    - Extract these data sets.
2. You must install Altair and altair_viewer as well as geopandas if it is not currently installed.
3. Before running, adjust the path variables in analyze.py to reflect the location of the
data sets. Specifically, the variables are:
    - AREA_DATA_PATH: points to the cancer data table titled "byarea.txt"
    - SITE_DATA_PATH: points to the cancer data tables titled "bysite.txt"
    - COUNTY_DATA_PATH: points to the cancer data table titled "byarea_county.txt"
    - SHP_DATA_PATH: points to the cb_2020_us_county_20m.shp. NOTE: the other files from the census data zip must
        be in the same directory as the shape file!
4. Run analyze.py.
5. Observe the resulting html files in a web browser. Ensure that javascript is not blocked on your browser.

## Note
1. Please refer to `CSE163-ProjectReport` for introduction, background, methodology, and solution, etc. about this project.
