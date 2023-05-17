import os

import pandas as pd


def read_mzmine3_peaktable(path, raw_peak_table):

    # Read in thee MZMine3 peak table

    # list all files within the directory
    print(path)

    # change the working directory
    os.chdir(path)

    # read in the peak table from the working directory
    peak_table = pd.read_csv(raw_peak_table)

    # set the row indices to be the MZMine3 peak ID numbers
    peak_table = peak_table.set_index("id")

    return peak_table
