import os

import pandas as pd
import plotly.express as px

from src.assign_global_variables import path, Media_identifier, QC_identifier


def plot_rsd_vs_rt(
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    peak_info: pd.DataFrame,
    show_plot: bool
):

    """Creates a simple scatter plot for each sample group in the dataset of the feature RSD vs RT to assess feature
    reproducibility across the chromatogram. A new directory is made within the working directory to save the plots into.
    """

    # extract all RTs as a series
    RT = peak_info[["rt"]].squeeze()

    if Media_identifier == QC_identifier:

        all_stats = pd.concat([Bio_stats, QC_stats], axis=1)

    else:

        all_stats = pd.concat([Bio_stats, Media_stats, QC_stats], axis=1)


    # get all columns that contain rsd information
    all_stats = all_stats[[s for s in all_stats.columns if "rsd" in s]]

    # add the RT series info as a new column in the rsd df
    all_stats = pd.concat([all_stats, RT], axis=1)

    # make a new directory to store graphs in
    if os.path.exists(path + "RSD_plots/") == False:

        os.mkdir(path + "RSD_plots/")

    # Make an RSD vs RT plot for each group
    for c in all_stats.columns[0 : (len(all_stats.columns) - 1)]:

        fig = px.scatter(all_stats, x="rt", y=c)

        if show_plot == True:

            fig.show()

        fig.write_html(path + "RSD_plots/" + c + ".html")
