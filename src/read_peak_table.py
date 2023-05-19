import os

import pandas as pd


def read_mzmine3_peaktable(path: str, raw_peak_table: str):

    """"Takes a string filepath (path) and string filename (raw_peak_table) of a csv MZMine3 peak table this and returns
     it as a Pandas dataframe after setting the row indices to the row/feature ID numbers exported by MZMine3 """

    # Read in the MZMine3 peak table

    # list all files within the directory
    print("current working directory is...\n" + path)

    # change the working directory
    os.chdir(path)

    # read in the peak table from the working directory
    peak_table = pd.read_csv(raw_peak_table)

    # set the row indices to be the MZMine3 peak ID numbers
    peak_table = peak_table.set_index("id")

    return peak_table
