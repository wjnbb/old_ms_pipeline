import os
import pandas as pd
import plotly.express as px
from src.assign_global_variables import path


def plot_weighted_distance_score(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):
        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    weighted_distance_score = peak_quality_df["alignment_scores:weighted_distance_score"]

    fig = px.histogram(
        weighted_distance_score,
        x="alignment_scores:weighted_distance_score",
        title="weighted_distance_score histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/weighted_distance_score_histogram.html")

    return weighted_distance_score


def plot_align_extra_features(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if os.path.exists(path + "peak_quality_plots/all_filtered_peaks/") == False:
        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    align_extra_features = peak_quality_df["alignment_scores:align_extra_features"]

    fig = px.histogram(
        align_extra_features,
        x="alignment_scores:align_extra_features",
        title="align_extra_features histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/align_extra_features_histogram.html")

    return align_extra_features


def plot_aligned_features_n(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):
        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    aligned_features_n = peak_quality_df["alignment_scores:aligned_features_n"]

    fig = px.histogram(
        aligned_features_n,
        x="alignment_scores:aligned_features_n",
        title="aligned_features_n histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/aligned_features_n_histogram.html")

    return aligned_features_n


def plot_alignment_rate(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):
        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    alignment_rate = (peak_quality_df["alignment_scores:rate"])*100

    fig = px.histogram(
        alignment_rate,
        x="alignment_scores:rate",
        title="alignment_rate histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/alignment_rate_histogram.html")

    return alignment_rate


def plot_ms2_n_signals(
        peak_quality_df:pd.DataFrame,
        aligned_peak_info:pd.DataFrame,
        show_plot:bool
    ):

    # extract all RTs as a series
    RT = aligned_peak_info[["rt"]].squeeze()

    ms2_n_signals = peak_quality_df["spectral_db_matches:n_matching_signals"]

    # add the RT series info as a new column in the rsd df
    avg_peak_quality = pd.concat([ms2_n_signals, RT], axis=1)
    avg_peak_quality.columns.values[0] = "MS2 n signals"

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):
        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="MS2 n signals",
                     title="Average MS2 matching signals vs RT"
    )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_MS2 matching signals_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="MS2 n signals",
                       title="average MS2 matching signals histogram"
    )

    if show_plot == True:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/average_MS2_matching_signals_histogram.html")

    return ms2_n_signals


def plot_height(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):
    avg_height = pd.Series(peak_quality_df.mean(axis=1), name="height")

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/"):
        os.mkdir(path + "peak_quality_plots/")

    fig = px.histogram(
                       avg_height,
                       x="height",
                       title="Average height histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/average_height_histogram.html")

    return avg_height


def plot_area(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    avg_area = pd.Series(peak_quality_df.mean(axis=1), name="area")

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):

        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    fig = px.histogram(
                       avg_area,
                       x="area",
                       title="Average area histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/average_area_histogram.html")

    return avg_area


def plot_ms2_apex_dist(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    avg_ms2_apex_dist = pd.Series(peak_quality_df.mean(axis=1), name="ms2_apex_dist")

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):

        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    fig = px.histogram(
                       avg_ms2_apex_dist,
                       x="ms2_apex_dist",
                       title="Average ms2_apex_dist histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/average_ms2_apex_dist_histogram.html")

    return avg_ms2_apex_dist

def plot_frag_scans(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    avg_frag_scans = pd.Series(peak_quality_df.mean(axis=1), name="frag_scans")
    avg_frag_scans = avg_frag_scans.fillna(0)

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):

        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    fig = px.histogram(
                       avg_frag_scans,
                       x="frag_scans",
                       title="Average frag_scans histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/average_frag_scans_histogram.html")

    return avg_frag_scans

def plot_charge(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    avg_charge = pd.Series(peak_quality_df.mean(axis=1), name="charge")
    avg_charge = avg_charge.fillna(0)

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/"):

        os.mkdir(path + "peak_quality_plots/")

    fig = px.histogram(
                       avg_charge,
                       x="charge",
                       title="Average charge histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/average_charge_histogram.html")

    return avg_charge


def plot_isotopes(
        peak_quality_df: pd.DataFrame,
        show_plot: bool
):

    avg_isotopes = pd.Series(peak_quality_df.mean(axis=1), name="isotopes")
    avg_isotopes = avg_isotopes.fillna(0)

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/all_filtered_peaks/"):

        os.mkdir(path + "peak_quality_plots/all_filtered_peaks/")

    fig = px.histogram(
                       avg_isotopes,
                       x="isotopes",
                       title="Average isotope histogram"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/all_filtered_peaks/average_isotope_histogram.html")

    return avg_isotopes

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
    if not os.path.exists(path + "peak_quality_plots/"):

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="FWHM",
                     title="Average FWHM vs RT"
    )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_FWHM_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="FWHM",
                       title="Average FWHM histogram"
    )

    if show_plot:
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
    if not os.path.exists(path + "peak_quality_plots/"):

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
    if not os.path.exists(path + "peak_quality_plots/"):

        os.mkdir(path + "peak_quality_plots/")

    fig = px.scatter(
                     avg_peak_quality,
                     x="rt",
                     y="tailing_factor",
                     title="Average tailing factor vs RT"
                     )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_tailing_factor_vs_RT.html")

    fig = px.histogram(
                       avg_peak_quality,
                       x="tailing_factor",
                       title="Average tailing factor histogram"
    )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/average_tailing_factor_histogram.html")

    return avg_peak_quality

def plot_standards_isotopes(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="Isotopes",
        title="Average Isotope Number Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_isotope_histogram.html")


def plot_standards_charge(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="Charge",
        title="Asymmetry Charge Value Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_Charge_histogram.html")


def plot_standards_frag_scans(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="Fragment Scans",
        title="Average Number of MS2 Scans Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_Fragment_Scans_histogram.html")


def plot_standards_ms2_apex_dist(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="MS2 Apex Distance",
        title="Average MS2 Apex Distance Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_MS2_apex_dist_histogram.html")


def plot_standards_area(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="Area",
        title="Average Area Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_area_histogram.html")


def plot_standards_height(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.histogram(
        major_ion_matches,
        x="Avg_height",
        title="Average Height Histogram for Standards Major/Protonated Ions",
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/average_standards_height_histogram.html")


def plot_standards_fwhm(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
    ):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.scatter(
                     major_ion_matches,
                     x="rt",
                     y="FWHM",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="FWHM vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_FWHM_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="FWHM",
                       title="Asymmetry Factor Histogram for Standards Major/Protonated Ions",
                       nbins=round((len(major_ion_matches))/5)
                       )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_average_FWHM_histogram.html")



def plot_standards_asymmetry(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):

    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.scatter(major_ion_matches,
                     x="rt",
                     y="asymmetry_factor",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="Asymmetry Factor vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot:

        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_asymmetry_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="asymmetry_factor",
                       title="Asymmetry Factor Histogram for Standards Major/Protonated Ions"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_average_asymmetry_histogram.html")


def plot_standards_tailing(
        major_ion_matches: pd.DataFrame,
        show_plot: bool
):
    # make a new directory to store graphs in
    if not os.path.exists(path + "peak_quality_plots/standards/"):

        os.mkdir(path + "peak_quality_plots/standards/")

    fig = px.scatter(
                     major_ion_matches,
                     x="rt",
                     y="tailing_factor",
                     color=major_ion_matches["Standard"],
                     size=major_ion_matches["Avg_height"],
                     title="Tailing Factor vs RT for Standards Major/Protonated Ions"
                     )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_tailing_vs_RT.html")

    fig = px.histogram(
                       major_ion_matches,
                       x="tailing_factor",
                       title="Tailing Factor Histogram for Standards Major/Protonated Ions"
    )

    if show_plot:
        fig.show()

    fig.write_html(path + "peak_quality_plots/standards/standards_average_tailing_histogram.html")
