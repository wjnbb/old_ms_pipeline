import pandas as pd
from src.assign_global_variables import Bio_identifier, Media_identifier, Blank_identifier, QC_identifier, MS_system, batch_name


def get_multi_group_heights(
    height_df: pd.DataFrame, Bio: list, Media: list, Blanks: list, QCs: list
):

    """Takes a MZMine3 peak height Pandas dataframe and lists of the samples contained within the biological,
    media/control, blank and QC sample groups. Returns a tuple of four Pandas dataframes dividing the peak height data
    into their separate groups."""

    Bio_table = height_df.loc[
        :, [c for c in height_df.columns if all(b in c for b in Bio)]
    ]
    Media_table = height_df.loc[
        :, [c for c in height_df.columns if all(m in c for m in Media)]
    ]
    Blank_table = height_df.loc[
        :, [c for c in height_df.columns if all(b in c for b in Blanks)]
    ]
    QC_table = height_df.loc[
        :, [c for c in height_df.columns if all(q in c for q in QCs)]
    ]

    return Bio_table, Media_table, Blank_table, QC_table

def get_single_group_heights(
    height_df: pd.DataFrame, names: list
):

    """Takes a MZMine3 peak height Pandas dataframe and lists of the samples contained within the biological,
    media/control, blank and QC sample groups. Returns a tuple of four Pandas dataframes dividing the peak height data
    into their separate groups."""

    #Get sample names for the group from the identifier
    Media_names = [c for c in names if Media_identifier in c]

    if MS_system == "Sciex":
        Media_cols = [(batch_name+"-") + c for c in Media_names]
        # Add datafile: to the start of the sample name
        Media_cols = ["datafile:" + c for c in Media_cols]
        # Add :height to the end of the sample name
        Media_cols = ["{}{}".format(c, ":height") for c in Media_cols]
        # Get the sample group only peak height table
        Media_table = height_df.loc[:, Media_cols]

    else:

        #Add datafile: to the start of the sample name
        Media_cols = ["datafile:" + c for c in Media_names]
        #Add :height to the end of the sample name
        Media_cols = ["{}{}".format(c, ":height") for c in Media_cols]
        #Get the sample group only peak height table
        Media_table = height_df.loc[:, Media_cols]

    #Get sample names for the group from the identifier
    Bio_names = [c for c in names if Bio_identifier in c]

    if MS_system == "Sciex":
        Bio_cols = [(batch_name+"-") + c for c in Bio_names]
        # Add datafile: to the start of the sample name
        Bio_cols = ["datafile:" + c for c in Bio_cols]
        # Add :height to the end of the sample name
        Bio_cols = ["{}{}".format(c, ":height") for c in Bio_cols]
        # Get the sample group only peak height table
        Bio_table = height_df.loc[:, Bio_cols]

    else:

        #Add datafile: to the start of the sample name
        Bio_cols = ["datafile:" + c for c in Bio_names]
        #Add :height to the end of the sample name
        Bio_cols = ["{}{}".format(c, ":height") for c in Bio_cols]
        #Get the sample group only peak height table
        Bio_table = height_df.loc[:, Bio_cols]

    #Get sample names for the group from the identifier
    Blank_names = [c for c in names if Blank_identifier in c]

    if MS_system == "Sciex":
        Blank_cols = [(batch_name+"-") + c for c in Blank_names]
        # Add datafile: to the start of the sample name
        Blank_cols = ["datafile:" + c for c in Blank_cols]
        # Add :height to the end of the sample name
        Blank_cols = ["{}{}".format(c, ":height") for c in Blank_cols]
        # Get the sample group only peak height table
        Blank_table = height_df.loc[:, Blank_cols]

    else:

        #Add datafile: to the start of the sample name
        Blank_cols = ["datafile:" + c for c in Blank_names]
        #Add :height to the end of the sample name
        Blank_cols = ["{}{}".format(c, ":height") for c in Blank_cols]
        #Get the sample group only peak height table
        Blank_table = height_df.loc[:, Blank_cols]

    #Get sample names for the group from the identifier
    QC_names = [c for c in names if QC_identifier in c]

    if MS_system == "Sciex":

        #add the batch name to the column name
        QC_cols = [(batch_name+"-") + c for c in QC_names]
        # Add datafile: to the start of the sample name
        QC_cols = ["datafile:" + c for c in QC_cols]
        # Add :height to the end of the sample name
        QC_cols = ["{}{}".format(c, ":height") for c in QC_cols]
        # Get the sample group only peak height table
        QC_table = height_df.loc[:, QC_cols]

    else:

        #Add datafile: to the start of the sample name
        QC_cols = ["datafile:" + c for c in QC_names]
        #Add :height to the end of the sample name
        QC_cols = ["{}{}".format(c, ":height") for c in QC_cols]
        #Get the sample group only peak height table
        QC_table = height_df.loc[:, QC_cols]


    return Bio_table, Media_table, Blank_table, QC_table