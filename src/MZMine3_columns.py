import pandas as pd


def mzmine3_cols(peak_table: pd.DataFrame):

    """ Takes a MZMine3 peak table as a Pandas dataframe and extracts all the column names as a list."""

    # get all column names to allow subsequent organisation of samples names and table subsections

    pt_cols = list(peak_table.columns)
    return pt_cols
