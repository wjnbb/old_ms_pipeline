from src.assign_global_variables import path
import os
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_peak_height_hist(df: pd.DataFrame, plot_name : str, show_fig: bool):

    """ Makes a simple histogram of peak height data when supplied with a table containing average peak heights."""

    if type(df) is tuple:

        df = pd.concat([df[0], df[1], df[2]], axis=1)

        # filter so just the avg peak height data is remaining
        df = df[[i for i in df.columns if "avg" in i]]

    if(os.path.exists(path + "/histograms") == False):

        os.mkdir(path + "/histograms")

    #melt the remaining data so all peak height info is in one column
    df = pd.melt(df)

    #initialise plot
    fig = make_subplots(
        rows=1,
        cols=1,
    )

    #add the data to the plot
    fig.add_trace(
        go.Histogram(x=df.value, nbinsx=100), row=1, col=1
    )

    fig.update_layout(
        title=dict(text=plot_name),
        xaxis_title="Average Peak Height",
        yaxis_title="Count"
    )

    #fig.write_image(plot_name + ".png")
    fig.write_html("histograms/" + plot_name + ".html")

    if show_fig == "True":

        fig.show()