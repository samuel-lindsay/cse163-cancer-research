"""
Sam Lindsay and Peter Xu
CSE 163
This file contains all the testing programs for all functions in Utils
class from utilities file.
"""


from cse163_utils import assert_equals
from utilities import Utils
import pandas as pd


def test_get_mir():
    """
    Test the get_mir method in Utils class. Report errors if get_mir returns
    unexpected results. If we have both mortality and incidence rate, get_mir
    should return a float. There will be no other type of return due to the
    cleaning form remove_rows and inner join type.
    """
    data = pd.read_csv("testing_data\\get_mir_test_data.txt")
    mir_data = Utils.get_mir(data, on=["AREA", "YEAR", "SITE"],
                             rate_col="AGE_ADJUSTED_RATE")
    assert_equals(3, len(mir_data))
    assert_equals(0.450831, mir_data["MIR"][0])
    assert_equals(0.448444, mir_data["MIR"][1])
    assert_equals(0.440550, mir_data["MIR"][2])


def test_remove_rows():
    """
    Test the remove_rows method in Utils class. Report errors if remove_rows
    returns unexpected results. The function remove_rows should remove all
    rows with any character that represents a None value. If all rows are
    filled with meaningful entry, remove_rows does nothing.
    """
    test_df = pd.read_csv("testing_data\\remove_rows_test_data.txt")
    exp_df1 = test_df.loc[[0, 2], :]
    assert_equals(exp_df1, Utils.remove_rows(test_df, ["+", ".", "~", "-"]))
    exp_df2 = test_df.loc[0:4, :]
    assert_equals(exp_df2, Utils.remove_rows(test_df, ["+"]))
    exp_df3 = test_df
    assert_equals(exp_df3, Utils.remove_rows(test_df, []))


def test_filter_sex_site_race():
    """
    Test the filter_sex_site_race function in Utils class. Report errors if
    the function returns unexpected results. By default, the filter_sex_site
    _race function should only include rows in a dataset that represent data
    for all cancer sites, all sexes, and all races.
    """
    data = pd.read_csv("testing_data\\filter_data.txt", sep="|")

    filter_sex = data["SEX"] == "Female"
    filter_site = data["SITE"] == "Pancreas"
    filter_race = data["RACE"] == "Hispanic"

    assert_equals(data[filter_sex],
                  Utils.filter_sex_site_race(data, sex="Female", site=None,
                                             race=None))
    assert_equals(data[filter_site],
                  Utils.filter_sex_site_race(data, sex=None, site="Pancreas",
                                             race=None))
    assert_equals(data[filter_race],
                  Utils.filter_sex_site_race(data, sex=None, site=None,
                                             race="Hispanic"))
    assert_equals(data[filter_sex & filter_site & filter_race],
                  Utils.filter_sex_site_race(data, sex="Female",
                                             site="Pancreas",
                                             race="Hispanic"))


def test_filter_alaska_hawaii():
    """
    Test teh filter_alaska_hawaii function in Utils class. Report errors if
    the function returns unexpected results. The returned DataFrame object
    should exclude all rows representing data from Alaska or Hawaii.
    """
    data = pd.read_csv("testing_data\\filter_data.txt", sep="|")
    filtered = data.loc[0:4, :]
    assert_equals(filtered, Utils.filter_alaska_hawaii(data, "AREA"))


def main():
    test_get_mir()
    test_remove_rows()
    test_filter_sex_site_race()
    test_filter_alaska_hawaii()


if __name__ == '__main__':
    main()
