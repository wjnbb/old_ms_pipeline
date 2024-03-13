from typing import Union

import pandas as pd

from src.assign_global_variables import (
    Bio_identifier,
    Blank_identifier,
    Media_identifier,
    QC_identifier,
)


def avg_sd_rsd(df: pd.DataFrame, groups: Union[list, str], grp_names: list):

    """Takes the peak height Pandas dataframe for a sample group (Biolgical, Media/Control, Blank or QC), the group identifier
    (for blanks and QCs) or list of subgroups (for biological or media/controls) as well as the list of all samples names
    in the group. The peak height average, standard deviation and relative standard deviation are calculated for each feature
    in each group/subgroup. Returns a Pandas dataframe containing all calculated statistics for the group."""

    if df.empty:
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
            all_stats.insert(0, (g + "_avg"), grp_avg)
            all_stats.insert(0, (g + "_sd"), grp_sd)
            all_stats.insert(0, (g + "_rsd"), grp_rsd)

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
            all_stats.insert(0, (groups + "_avg"), grp_avg)
            all_stats.insert(0, (groups + "_sd"), grp_sd)
            all_stats.insert(0, (groups + "_rsd"), grp_rsd)

        if len([s for s in grp_names if Media_identifier in s]) >= 1:
            all_stats.insert(0, (groups + "_avg"), grp_avg)
            all_stats.insert(0, (groups + "_sd"), grp_sd)
            all_stats.insert(0, (groups + "_rsd"), grp_rsd)

    return all_stats



def avg_sd_rsd_binary(df: pd.DataFrame, groups: Union[list, str], grp_names: list):

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

            if Bio_identifier not in grp_names == False:
                all_stats.insert(0, "Blank_avg", grp_avg)
                all_stats.insert(0, "Blank_sd", grp_sd)
                all_stats.insert(0, "Blank_rsd", grp_rsd)
                break

            # add the newly calculated stats to the stats table
            all_stats.insert(0, (g + "_avg"), grp_avg)
            all_stats.insert(0, (g + "_sd"), grp_sd)
            all_stats.insert(0, (g + "_rsd"), grp_rsd)



    else:

        # calculate the stats for the group if it is all one
        all_stats = pd.DataFrame()

        grp_avg = df.mean(axis=1)
        grp_sd = df.std(axis=1)
        grp_rsd = (grp_sd / grp_avg) * 100

        if Bio_identifier not in grp_names:

            all_stats.insert(0, "Blank_avg", grp_avg)
            all_stats.insert(0, "Blank_sd", grp_sd)
            all_stats.insert(0, "Blank_rsd", grp_rsd)

        if len([s for s in grp_names if Bio_identifier in s]) >= 1:
            all_stats.insert(0, (groups + "_avg"), grp_avg)
            all_stats.insert(0, (groups + "_sd"), grp_sd)
            all_stats.insert(0, (groups + "_rsd"), grp_rsd)

    return all_stats
