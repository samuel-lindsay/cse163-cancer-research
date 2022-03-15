import pandas as pd


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

    def filter_sex_site(data, site="All Cancer Sites Combined",
                        sex="Male and Female"):
        """
        Takes in cancer data as well as a site and sex value.
        Filters data by site and sex, then returns filtered data.
        """
        site_filter = data["SITE"] == site
        sex_filter = data["SEX"] == sex
        return data[site_filter & sex_filter]

    def filter_alaska_hawaii(data, colname):
        """
        Takes in cancer data, returns data without Alaska or Hawaii.
        Also takes in a column name which specifies which columns contains
        the state data (in its USPS abbreviation)
        """
        ak_filter = data[colname] != "AK"
        hi_filter = data[colname] != "HI"
        return data[ak_filter & hi_filter]
