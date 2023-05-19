import pandas as pd


def QC_Filter(QC_stats: pd.DataFrame, QC_RSD_thresh: int) -> list:

    """Takes a Pandas dataframe of QC sample peak height stats and a percentage RSD threshold and returns a list of feature/rows
    indices which don't meet the QC sample RSD threshold."""

    # Find all row indices for which the QC rsd was less than the user specified threshold
    QC_i_filt = QC_stats.index[(QC_stats.iloc[:, 0]) <= QC_RSD_thresh].tolist()

    print(str(len(QC_i_filt)) + " features left after QC filtering.")
    print(str((len(QC_i_filt) / len(QC_stats)) * 100) + "% of feature list remaining")

    return QC_i_filt
