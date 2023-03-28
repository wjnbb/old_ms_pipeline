import pandas as pd

from src.assign_global_variables import (
    Bio_identifier,
    Blank_identifier,
    Media_identifier,
    QC_identifier,
)

# Calculates the avg, sd and rsd for any sample group


def avg_sd_rsd(df, groups, grp_names):

    if(df.empty):
        all_stats = pd.DataFrame()
        return all_stats

    # checks if the group is made of many subgroups each requiring their own average or if the group is all one

    if isinstance(groups, list):

        all_stats = pd.DataFrame()

        for g in groups:

            # get all columns for that biological group within the group
            grp_cols = df[[s for s in df.columns if g in s]]

            # calculate the peak height avg, sd and rsd for the current group
            grp_avg = grp_cols.mean(axis=1)
            grp_sd = grp_cols.std(axis=1)
            grp_rsd = (grp_sd / grp_avg) * 100

            # add the newly calculated stats to the stats table
            all_stats.insert(0, (g + "avg"), grp_avg)
            all_stats.insert(0, (g + "sd"), grp_sd)
            all_stats.insert(0, (g + "rsd"), grp_rsd)

    else:

        # calculate the stats for the group if it is all one
        all_stats = pd.DataFrame()

        grp_avg = df.mean(axis=1)
        grp_sd = df.std(axis=1)
        grp_rsd = (grp_sd / grp_avg) * 100

        # check if the group is Bio/Media/Blank or QC and attach appropriate label to column headers
        if len([s for s in grp_names if QC_identifier in s]) >= 1:

            all_stats.insert(0, "QC_avg", grp_avg)
            all_stats.insert(0, "QC_sd", grp_sd)
            all_stats.insert(0, "QC_rsd", grp_rsd)

        if len([s for s in grp_names if Blank_identifier in s]) >= 1:

            all_stats.insert(0, "Blank_avg", grp_avg)
            all_stats.insert(0, "Blank_sd", grp_sd)
            all_stats.insert(0, "Blank_rsd", grp_rsd)

        if len([s for s in grp_names if Bio_identifier in s]) >= 1:
            all_stats.insert(0, (groups + "avg"), grp_avg)
            all_stats.insert(0, (groups + "sd"), grp_sd)
            all_stats.insert(0, (groups + "rsd"), grp_rsd)

        if len([s for s in grp_names if Media_identifier in s]) >= 1:
            all_stats.insert(0, (groups + "avg"), grp_avg)
            all_stats.insert(0, (groups + "sd"), grp_sd)
            all_stats.insert(0, (groups + "rsd"), grp_rsd)

    return all_stats
