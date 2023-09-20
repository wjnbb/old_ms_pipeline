import pandas as pd
import numpy as np

from src.assign_global_variables import Blank_thresh

def blank_filter(
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
) -> list:
    """
        Takes the peak height stats (avg, sd, rsd) calculated for each sample group and identifies all feature rows for which no
    biological, media or QC sample average height in the dataset exceeded a minimum FC as specified by the Blank_thresh
    variable versus the average height of the blank samples and returns a list of the indices of those rows."
    """

    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats], axis=1)
    all_stats = all_stats[[s for s in all_stats.columns if "avg" in s]]

    all_stats = all_stats.fillna(10)
    Blank_stats["Blank_avg"] = Blank_stats["Blank_avg"].fillna(10)

    B_FC_table = pd.DataFrame()

    # calculate FC against the blank average for all bio,media and QC triplicates
    for b in all_stats.columns:

        print("Printing column for BFC calculation...." + str(b))

        bios = all_stats[[s for s in all_stats.columns if b in s]]
        bios = bios.squeeze()
        B_FC = bios / (Blank_stats["Blank_avg"].squeeze())
        print("Printing calculated BFC column" + str(B_FC))
        B_FC_table.insert(0, ("FC" + b), B_FC)

    Blank_i_filt = []

    for r in B_FC_table.index:

        if np.nanmax((B_FC_table.loc[r, :])) >= Blank_thresh:

            Blank_i_filt.append(r)

    print("")
    print("Blank threshold applied for filtering is " + str(Blank_thresh))
    print(str(len(Blank_i_filt)) + " features left after blank filtering")
    print(
        str((len(Blank_i_filt) / len(all_stats)) * 100)
        + " % of features left after blank filtering"
    )

    return Blank_i_filt
