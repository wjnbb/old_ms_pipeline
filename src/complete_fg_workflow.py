import pandas as pd

from src.Avg_SD_RSD_calcs import avg_sd_rsd
from src.Blank_Filtering import blank_filter
from src.detect_sample_groups import detect_sample_groups
from src.dilution_series_analysis import dil_series_analyser
from src.Export_Peak_Table import export_PT_noFC
from src.feature_group_stats_summary import feature_group_summariser
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Fraction_filter import fraction_filter_noFC
from src.get_group_heights import (
    get_single_group_heights,
    get_single_group_areas
)

from src.ID_levels import ID_levels
from src.MZMine3_columns import mzmine3_cols
from src.MZMine3_module_divider import divide_mzmine3_table
from src.plot_peak_quality import (
    plot_fwhm,
    plot_asymmetry,
    plot_tailing,
    plot_isotopes,
    plot_charge,
    plot_frag_scans,
    plot_ms2_apex_dist,
    plot_height,
    plot_area,
    plot_ms2_n_signals,
    plot_alignment_rate,
    plot_aligned_features_n,
    plot_align_extra_features,
    plot_weighted_distance_score
)
from src.Plot_RSDs import plot_rsd_vs_rt
from src.read_peak_table import read_mzmine3_peaktable
from src.sample_names import get_sample_names
from src.Standards import (
   chloramphenicol,
   cycloheximide,
   hygromycin,
   imipenem,
   neomycin,
   nystatin,
   polymyxin_b,
   tetracycline,
   fosfomycin,
   lincomycin,
   paromomycin,
   penicillin_g,
   rifampicin,
   vancomycin,
   tobramycin,
   thiostrepton
)
from src.assign_global_variables import (
    path,
    peaklist,
    Blank_identifier,
    QC_identifier
)

#def complete_fg_workflow(dataset:str):

    print(f"Printing path at the start of the dataset loop after assign global variable changes {path}")

    #Read in and organise the peak table and detect sample groups
    mzmine3 = read_mzmine3_peaktable(path, peaklist)
    cols = mzmine3_cols(mzmine3)
    mods = divide_mzmine3_table(mzmine3, cols)
    names = get_sample_names(mods[6])
    groups = detect_sample_groups(names)
    heights = get_single_group_heights(mods[6], names)
    areas = get_single_group_areas(mods[13], names)

    #Calculate avg, sd and rsd for all peak heights for all features in all groups
    bio_height_stats = avg_sd_rsd(heights[0], groups[4], groups[0])
    media_height_stats = avg_sd_rsd(heights[1], groups[5], groups[1])
    blank_height_stats = avg_sd_rsd(heights[2], Blank_identifier, groups[2])
    qc_height_stats = avg_sd_rsd(heights[3], QC_identifier, groups[3])

    #Calculate avg, sd and rsd for all peak areas for all features in all groups
    bio_areas_stats = avg_sd_rsd(areas[0], groups[4], groups[0])
    media_areas_stats = avg_sd_rsd(areas[1], groups[5], groups[1])
    blank_areas_stats = avg_sd_rsd(areas[2], Blank_identifier, groups[2])
    qc_areas_stats = avg_sd_rsd(areas[3], QC_identifier, groups[3])

    #Blank Filtering
    blank_i_filt = blank_filter(bio_height_stats, media_height_stats, qc_height_stats, blank_height_stats)
    bio_stats = single_table_filt(blank_i_filt[0], bio_height_stats)
    media_stats = single_table_filt(blank_i_filt[0], media_height_stats)
    qc_stats = single_table_filt(blank_i_filt[0], qc_height_stats)
    mods_blank_filt = module_tables_filt(blank_i_filt[0], mods)
    heights = module_tables_filt(blank_i_filt[0], heights)
    areas = module_tables_filt(blank_i_filt[0], areas)

    #plot feature reproducibility across the run
    plot_rsd_vs_rt(bio_stats, media_stats, qc_stats, mods_blank_filt[7], show_plot=True)

    #plot peak quality across the run and histograms of their distributions
    plot_height(mods_blank_filt[6], show_plot=True)
    areas = plot_area(mods_blank_filt[13], show_plot=True)
    fwhm = plot_fwhm(mods_blank_filt[8], mods_blank_filt[7], show_plot=True)
    asymmetry = plot_asymmetry(mods_blank_filt[9], mods_blank_filt[7], show_plot=True)
    tailing = plot_tailing(mods_blank_filt[10], mods_blank_filt[7], show_plot=True)
    charge = plot_charge(mods_blank_filt[11], show_plot=True)
    isotopes = plot_isotopes(mods_blank_filt[12], show_plot=True)
    frag_scans = plot_frag_scans(mods_blank_filt[14], show_plot=True)
    ms2_apex_dist = plot_ms2_apex_dist(mods_blank_filt[15], show_plot=True)
    ms2_n_signals = plot_ms2_n_signals(mods_blank_filt[1], mods_blank_filt[7], show_plot=True)
    alignment_rate = plot_alignment_rate(mods_blank_filt[3], show_plot=True)
    aligned_features_n = plot_aligned_features_n(mods_blank_filt[3], show_plot=True)
    align_extra_features = plot_align_extra_features(mods_blank_filt[3], show_plot=True)
    weighted_distance_score = plot_weighted_distance_score(mods_blank_filt[3], show_plot=True)

    #merge peak quality metrics
    peak_quality_metrics = (fwhm.merge(asymmetry,
                                       left_index=True,
                                       right_index=True)).merge(tailing,
                                                                left_index=True,
                                                                right_index=True)
    peak_quality_metrics = peak_quality_metrics.drop(columns=["rt_x", "rt_y", "rt"])
    peak_quality_metrics = pd.concat([peak_quality_metrics,
                                      pd.Series(areas, name="Area"),
                                      pd.Series(charge, name="Charge"),
                                      pd.Series(isotopes, name="Isotopes"),
                                      pd.Series(frag_scans, name="Fragment Scans"),
                                      pd.Series(ms2_apex_dist, name="MS2 Apex Distance"),
                                      pd.Series(ms2_n_signals, name="MS2 n matching signals"),
                                      pd.Series(alignment_rate, name="% presence in all samples"),
                                      pd.Series(aligned_features_n, name="Number of Aligned Features"),
                                      pd.Series(align_extra_features, name="Align Extra Features Number"),
                                      pd.Series(weighted_distance_score, name="Weighted Distance Score")
                                      ],
                                      axis=1)


    #Add levels of ID
    ID_levels(mods_blank_filt)

    #Export peak table for the whole dataset
    export_PT_noFC(
                     mods_blank_filt,
                     bio_stats,
                     media_stats,
                     qc_stats,
                     blank_height_stats,
                     heights,
                     peak_quality_metrics
                   )

    #export sample specific tables
    fraction_filter_noFC(
                         bio_stats,
                         groups[4],
                         mods_blank_filt,
                         peak_quality_metrics
                         )

    standards = [chloramphenicol,
                 cycloheximide,
                 hygromycin,
                 imipenem,
                 neomycin,
                 nystatin,
                 polymyxin_b,
                 tetracycline,
                 fosfomycin,
                 lincomycin,
                 paromomycin,
                 penicillin_g,
                 rifampicin,
                 vancomycin,
                 tobramycin,
                 thiostrepton]

    print(f"printing path after peak table export functions {path}")

    dil_series_analyser(standards, 5, bio_stats)
    #feature_group_summariser(path)