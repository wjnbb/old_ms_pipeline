import pandas as pd
import numpy as np

from src.assign_global_variables import Blank_thresh, QC_identifier, Media_identifier

def blank_filter(blank_stats: pd.DataFrame) -> list:
    """
        Takes the peak height stats (avg, sd, rsd) calculated for each sample group and identifies all feature rows for which no
    biological, media or QC sample average height in the dataset exceeded a minimum FC as specified by the Blank_thresh
    variable versus the average height of the blank samples and returns a list of the indices of those rows."
    """

    #Blank_stats = blank_stats
    total_features = len(blank_stats)
    blank_stats["Blank_avg"] = blank_stats["Blank_avg"].fillna(10)

    Blank_stats = blank_stats[blank_stats["Blank_avg"] > 10]

    Blank_i_filt = Blank_stats.index

    print("")
    print(str(total_features-(len(Blank_i_filt))) + " features left after blank filtering")
    print(
        str(((total_features-(len(Blank_i_filt)))/total_features)*100)
        + " % of features left after blank filtering"
    )

    return Blank_i_filt
