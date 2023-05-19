import pandas as pd

from assign_global_variables import Bio_identifier, Media_identifier, QC_identifier


def QC_normalisation(QC_stats: pd.DataFrame, Bio_stats: pd.DataFrame, Media_stats: pd.DataFrame):

    """Takes Pandas dataframes of peak height stats for QC, biological and media/control sample groups. Biological and
    media/control feature height averages are divided by the QC average height for that feature to generate a QC
    normalised peak height. Returns a tuple of pandas dataframes containing the QC normalised peak height data."""

    all_stats = pd.concat([QC_stats, Bio_stats, Media_stats], axis=1)
    all_stats = all_stats[[s for s in all_stats.columns if "avg" in s]]
    qch = QC_stats["QC_avg"].squeeze()
    norm_heights = pd.DataFrame()

    for c in all_stats.columns:

        c_height = all_stats[c].squeeze()
        n_height = c_height / qch
        norm_heights = pd.concat([norm_heights, n_height], axis=1)

    norm_heights.columns = all_stats.columns.tolist()

    Bio_heights_n = norm_heights[
        [c for c in norm_heights.columns if Bio_identifier in c]
    ]
    Media_heights_n = norm_heights[
        [c for c in norm_heights.columns if Media_identifier in c]
    ]
    QC_heights_n = norm_heights[[c for c in norm_heights.columns if QC_identifier in c]]

    return Bio_heights_n, Media_heights_n, QC_heights_n
