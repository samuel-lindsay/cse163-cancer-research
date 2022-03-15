"""
Sam Lindsay and Peter Xu
CSE 163
This file defines the Utils class, which contains methods related to cleaning
and preparing the cancer data set.
"""

import pandas as pd


class Utils:
    """
    Contains functions that cleans and prepares the cancer data for analysis
    and visualization.
    """
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

    def filter_sex_site_race(data, site="All Cancer Sites Combined",
                             sex="Male and Female", race="All Races"):
        """
        Takes in cancer data as well as a site, sex, and race value.
        If any of site, sex, and race are not None, then the related column
        is filtered by the given value. Returns filtered data.
        """
        filters = []
        if site is not None:
            filters.append(data["SITE"] == site)
        if sex is not None:
            filters.append(data["SEX"] == sex)
        if race is not None:
            filters.append(data["RACE"] == race)

        if len(filters) == 0:
            return data
        else:
            final_filter = filters[0]
            for f in filters:
                final_filter = final_filter & f
            return data[final_filter]

    def filter_alaska_hawaii(data, colname):
        """
        Takes in cancer data, returns data without Alaska or Hawaii.
        Also takes in a column name which specifies which columns contains
        the state data (in its USPS abbreviation)
        """
        ak_filter = data[colname] != "AK"
        hi_filter = data[colname] != "HI"
        return data[ak_filter & hi_filter]
