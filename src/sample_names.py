import pandas as pd
from src.assign_global_variables import MS_system

def get_sample_names(height_df: pd.DataFrame):

    """Takes a pandas dataframe of MZMine3 peak height data and then extracts all the sample names in the batch from
    within the column headers. Returns a list of all the sample names. Must specify whether the data was collected on
    "Sciex" or "Agilent" for the names to be assigned correctly"""

    # Pattern match on column names in the peak height data frame
    # take everything after datafile: to get the sample names

    if MS_system == "Sciex":

        sample_names_full = [name.split(":")[1] for name in height_df.columns]
        sample_names = [name.split("-")[1] for name in sample_names_full]

        return sample_names

    if MS_system == "Agilent":

        sample_names = [name.split(":")[1] for name in height_df.columns]

        return sample_names
