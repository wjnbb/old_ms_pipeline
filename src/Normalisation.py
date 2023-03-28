import pandas as pd

from assign_global_variables import Bio_identifier, Media_identifier, QC_identifier


def QC_normalisation(QC_stats, Bio_stats, Media_stats):

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
