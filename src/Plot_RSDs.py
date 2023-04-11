import os
import pandas as pd
import plotly.express as px
from src.assign_global_variables import path

def plot_rsd_vs_rt(Bio_stats, Media_stats, QC_stats, peak_info):

    #extract all RTs as a series
    RT = peak_info[["rt"]].squeeze()

    #combine stats cols from biological, media and QC groups
    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats], axis=1)

    #get all columns that contain rsd information
    all_stats = all_stats[[s for s in all_stats.columns if "rsd" in s]]

    #add the RT series info as a new column in the rsd df
    all_stats = pd.concat([all_stats, RT], axis=1)

    #make a new directory to store graphs in
    os.mkdir(path + "RSD_plots/")

    #Make an RSD vs RT plot for each group
    for c in all_stats.columns[0:(len(all_stats.columns) - 1)]:

        fig = px.scatter(all_stats, x="rt", y=c)
        fig.show()
        fig.write_html(path + "RSD_plots/" + c + ".html")



