import pandas as pd


class Utils:
    def getmir(data, on, desiredCol):
        """
        Takes in the already cleaned data. Given a set of columns to merge
        on, and desired col. it splits the data into mortality and
        incidence rows, then merges together based on the keys. Then it
        calculates an MIR and appends it to the data set with a new column.
        Returns the data with the MIR.
        """
        mortality = data[data["EVENT_TYPE"] == "Mortality"]
        incidence = data[data["EVENT_TYPE"] == "Incidence"]
        joined = pd.merge(mortality, incidence, how='inner', on=on)
        joined["MIR"] = joined[desiredCol + "_x"]/joined[desiredCol + "_y"]
        return joined

    def removeRows(data, chars):
        """
        Filters rows based on a ser
        """
        filter = data != chars[0]  # get base filter
        for c in chars:
            filter = filter & data != c
        return data[filter.all(1)]
