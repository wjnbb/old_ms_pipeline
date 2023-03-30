import pandas as pd

from assign_global_variables import Blank_thresh


def blank_filter(
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
) -> list:
    """
    Identifies all features rows for which no biological, media or QC sample height in the dataset exceeded a FC of 10
    versus the average intensity of the blank samples and returns the indices of those rows."
    """

    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats], axis=1)
    all_stats = all_stats[[s for s in all_stats.columns if "avg" in s]]

    Blank_stats["Blank_avg"] = Blank_stats["Blank_avg"].fillna(10)

    B_FC_table = pd.DataFrame()

    # calculate FC against the blank average for all AS23/media triplicates
    for b in all_stats.columns:

        print(b)
        bios = all_stats[[s for s in all_stats.columns if b in s]]
        bios = bios.squeeze()
        B_FC = bios / (Blank_stats["Blank_avg"].squeeze())
        B_FC_table.insert(0, ("FC" + b), B_FC)

    Blank_i_filt = []

    for r in B_FC_table.index:

        if max((B_FC_table.loc[r, :])) >= Blank_thresh:

            Blank_i_filt.append(r)

    print(str(len(Blank_i_filt)) + " features left after blank filtering")
    print(
        str((len(Blank_i_filt) / len(all_stats)) * 100)
        + " % of features left after blank filtering"
    )

    return Blank_i_filt
