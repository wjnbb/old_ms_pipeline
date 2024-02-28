import os
import pandas as pd
import plotly.express as px
from src.assign_global_variables import path

def plot_fwhm(
        peak_quality_df:pd.DataFrame,
        aligned_peak_info:pd.DataFrame,
        show_plot:bool
    ):

    # extract all RTs as a series
    RT = aligned_peak_info[["rt"]].squeeze()

    avg_peak_quality = peak_quality_df.mean(axis=1)

    # add the RT series info as a new column in the rsd df
    avg_peak_quality = pd.concat([avg_peak_quality, RT], axis=1)
    avg_peak_quality.columns.values[0] = "FWHM"

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="FWHM",
                     title="Average FWHM vs RT"
    )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_FWHM_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="FWHM",
                       title="Average FWHM histogram"
    )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/average_FWHM_histogram.html")

    return avg_peak_quality



def plot_asymmetry(
        peak_quality_df:pd.DataFrame,
        aligned_peak_info:pd.DataFrame,
        show_plot:bool
    ):

    # extract all RTs as a series
    RT = aligned_peak_info[["rt"]].squeeze()

    avg_peak_quality = peak_quality_df.mean(axis=1)

    # add the RT series info as a new column in the rsd df
    avg_peak_quality = pd.concat([avg_peak_quality, RT], axis=1)
    avg_peak_quality.columns.values[0] = "asymmetry_factor"

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="asymmetry_factor",
                     title="Average asymmetry factor vs RT"
                     )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_asymmetry_factor_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="asymmetry_factor",
                       title="Average asymmetry factor histogram"
    )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/average_asymmetry_factor_histogram.html")

    return avg_peak_quality


def plot_tailing(
        peak_quality_df:pd.DataFrame,
        aligned_peak_info:pd.DataFrame,
        show_plot:bool
    ):

    # extract all RTs as a series
    RT = aligned_peak_info[["rt"]].squeeze()

    avg_peak_quality = peak_quality_df.mean(axis=1)

    # add the RT series info as a new column in the rsd df
    avg_peak_quality = pd.concat([avg_peak_quality, RT], axis=1)
    avg_peak_quality.columns.values[0] = "tailing_factor"

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="tailing_factor",
                     title="Average tailing factor vs RT"
                     )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_tailing_factor_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="tailing_factor",
                       title="Average tailing factor histogram"
    )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_tailing_factor_histogram.html")

    return avg_peak_quality


def plot_standards_fwhm(
        major_ion_matches:pd.DataFrame,
        show_plot:bool
    ):

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     major_ion_matches,
                     x="rt",
                     y="FWHM",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="FWHM vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_FWHM_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="FWHM",
                       title="Asymmetry Factor Histogram for Standards Major/Protonated Ions",
                       nbins=round((len(major_ion_matches))/5)
                       )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_average_FWHM_histogram.html")



def plot_standards_asymmetry(
        major_ion_matches:pd.DataFrame,
        show_plot:bool
    ):

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(major_ion_matches,
                     x="rt",
                     y="asymmetry_factor",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="Asymmetry Factor vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot == True:

        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_asymmetry_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="asymmetry_factor",
                       title="Asymmetry Factor Histogram for Standards Major/Protonated Ions",
                       nbins=round((len(major_ion_matches))/5)
                       )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_average_asymmetry_histogram.html")


def plot_standards_tailing(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):
    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/") == False:
        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     major_ion_matches,
                     x="rt",
                     y="tailing_factor",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="Tailing Factor vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_tailing_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="tailing_factor",
                       title="Tailing Factor Histogram for Standards Major/Protonated Ions",
                       nbins=round((len(major_ion_matches))/5)
    )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards_average_tailing_histogram.html")