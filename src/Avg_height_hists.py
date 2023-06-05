from src.assign_global_variables import path
import os
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_peak_height_hist(df: pd.DataFrame, plot_name : str):

    """ Makes a simple histogram of peak height data when supplied with a table containing average peak heights."""

    if(os.path.exists(path + "/histograms") == False):

        os.mkdir(path + "/histograms")

    h4h = df

    #filter so just the avg peak height data is remaining
    h4h = df[[i for i in df.columns if "avg" in i]]

    #melt the remaining data so all peak height info is in one column
    h4h = pd.melt(h4h)

    #initialise plot
    fig = make_subplots(
        rows=1,
        cols=1,
    )

    #add the data to the plot
    fig.add_trace(
        go.Histogram(x=h4h.value, nbinsx=100), row=1, col=1
    )

    fig.update_layout(
        title=dict(text=plot_name),
        xaxis_title="Average Peak Height",
        yaxis_title="Count"
    )

    fig.write_image(plot_name + ".png")

    return fig.show()