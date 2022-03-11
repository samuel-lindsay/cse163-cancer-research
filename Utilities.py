import pandas as pd
import geopands as gpd


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

    
