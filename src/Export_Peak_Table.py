import pandas as pd
import datetime
import sqlite3

from src.assign_global_variables import batch_name


def export_PT_w_norm(
    module_tables: list,
    FC_Stats: pd.DataFrame,
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
    group_heights: tuple,
    norm_heights: tuple,
):

    """Takes the list of MZMine3 processing module Pandas dataframes, fold change stats dataframe, biological, media/control,
    QC and blank peak height stats dataframes, raw peak height data and normalised peak height data and exports it to a
    .xlsx file. Data is separated out into different sheets with key data from some of the MZMine3 processing modules
    collated into the first sheet. Each processing module from MZMine has the complete data in its own tab. The file is
    saved into the current working directory."""

    # Make the filtered data frame output
    # combine all the key_data columns from relevant tables into one data frame for sheet1
    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats, Blank_stats], axis=1)
    norm_heights_df = pd.concat(
        [norm_heights[0], norm_heights[1], norm_heights[2]], axis=1
    )
    heights = pd.concat(
        [group_heights[0], group_heights[1], group_heights[2], group_heights[3]], axis=1
    )

    Key_data = pd.DataFrame()

    Key_data = pd.concat(
        [
            ((module_tables[7])[["Level_of_ID", "mz", "rt", "feature_group"]]),
            (module_tables[1])[
                [
                    "spectral_db_matches:compound_name",
                    "spectral_db_matches:cosine_score",
                ]
            ],
            (module_tables[0])[
                [
                    "compound_db_identity:compound_name",
                    "compound_db_identity:mz_diff_ppm",
                ]
            ],
            (module_tables[2])[["formulas:formulas", "formulas:combined_score"]],
            (module_tables[3])[["alignment_scores:rate"]],
        ],
        axis=1,
    )

    Key_data = Key_data.rename({'spectral_db_matches:compound_name': "MS2 match",
                     'spectral_db_matches:cosine_score': "MS2 cosine score",
                     'compound_db_identity:compound_name': "MS1 match",
                     'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                     'formulas:formulas': 'Predicted MF',
                     'formulas:combined_score': 'MF score',
                     'alignment_scores:rate': "Alignment score"
                     }, axis='columns')

    PT_output = pd.ExcelWriter(
        "Final_Peak_Table_" + batch_name + ".xlsx", engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")
    (module_tables[3]).to_excel(PT_output, "Aligned_Feature_Data")
    FC_Stats.to_excel(PT_output, "FC_Data")
    (module_tables[1]).to_excel(PT_output, "MS2_Matching")
    (module_tables[0]).to_excel(PT_output, "MS1_Matching")
    (module_tables[2]).to_excel(PT_output, "MF_Prediction")
    (module_tables[4]).to_excel(PT_output, "IIN_Data")
    all_stats.to_excel(PT_output, "All_Stats")
    heights.to_excel(PT_output, "Raw Peak Heights")
    norm_heights_df.to_excel(PT_output, "Norm Peak Heights")

    PT_output.save()


#export_PT(mods_blank_filt, FC_table, bio_stats, media_stats, qc_stats, blank_stats, heights)
# module_tables = mods_blank_filt
# FC_Stats = FC_table
# Bio_stats = bio_stats
# Media_stats = media_stats
# QC_stats = qc_stats
# Blank_stats = blank_stats
# group_heights = heights


def export_PT(
    module_tables: list,
    FC_Stats: pd.DataFrame,
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
    group_heights: tuple,
):

    """Takes the list of MZMine3 processing module Pandas dataframes, fold change stats dataframe, biological, media/control,
    QC and blank peak height stats dataframes and raw peak height data and exports it to a .xlsx file. Data is separated out
    into different sheets with key data from some of the MZMine3 processing modules collated into the first sheet. Each
    processing module from MZMine has the complete data in its own tab. The file is saved into the current working directory."""

    # Make the filtered data frame output
    # combine all the key_data columns from relevant tables into one data frame for sheet1
    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats, Blank_stats], axis=1)

    heights = pd.concat(
        [group_heights[0], group_heights[1], group_heights[2], group_heights[3]], axis=1
    )

    Key_data = pd.DataFrame()

    Key_data = pd.concat(
        [
            ((module_tables[7])[["Level_of_ID", "mz", "rt", "feature_group"]]),
            (module_tables[4])[["ion_identities:ion_identities"]],
            (module_tables[1])[
                [
                    "spectral_db_matches:compound_name",
                    "spectral_db_matches:cosine_score",
                ]
            ],
            (module_tables[0])[
                [
                    "compound_db_identity:compound_name",
                    "compound_db_identity:mz_diff_ppm",
                ]
            ],
            (module_tables[2])[["formulas:formulas", "formulas:combined_score"]],
            (module_tables[3])[["alignment_scores:rate"]],
        ],
        axis=1,
    )

    Key_data = Key_data.rename({'ion_identities:ion_identities': "Adduct",
                     'spectral_db_matches:compound_name': "MS2 match",
                     'spectral_db_matches:cosine_score': "MS2 cosine score",
                     'compound_db_identity:compound_name': "MS1 match",
                     'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                     'formulas:formulas': 'Predicted MF',
                     'formulas:combined_score': 'MF score',
                     'alignment_scores:rate': "Alignment score"
                     }, axis='columns')

    PT_output = pd.ExcelWriter(
        "Final_Peak_Table_" + batch_name + ".xlsx", engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")
    (module_tables[3]).to_excel(PT_output, "Aligned_Feature_Data")
    FC_Stats.to_excel(PT_output, "FC_Data")
    (module_tables[1]).to_excel(PT_output, "MS2_Matching")
    (module_tables[0]).to_excel(PT_output, "MS1_Matching")
    (module_tables[2]).to_excel(PT_output, "MF_Prediction")
    (module_tables[4]).to_excel(PT_output, "IIN_Data")
    all_stats.to_excel(PT_output, "All_Stats")
    heights.to_excel(PT_output, "Raw Peak Heights")

    PT_output.close()


def export_PT_noFC(
    module_tables,
    Bio_stats,
    Media_stats,
    QC_stats,
    Blank_stats,
    group_heights,
):

    # Make the filtered data frame output
    # combine all the key_data columns from relevant tables into one data frame for sheet1
    all_stats = pd.concat([Bio_stats, Media_stats, QC_stats, Blank_stats], axis=1)

    heights = pd.concat(
        [group_heights[0], group_heights[1], group_heights[2], group_heights[3]], axis=1
    )

    Key_data = pd.DataFrame()

    Key_data = pd.concat(
        [
            ((module_tables[7])[["Level_of_ID", "mz", "rt", "feature_group"]]),
            (module_tables[4])[["ion_identities:ion_identities"]],
            (module_tables[1])[
                [
                    "spectral_db_matches:compound_name",
                    "spectral_db_matches:cosine_score",
                ]
            ],
            (module_tables[0])[
                [
                    "compound_db_identity:compound_name",
                    "compound_db_identity:mz_diff_ppm",
                ]
            ],
            (module_tables[2])[["formulas:formulas", "formulas:combined_score"]],
            (module_tables[3])[["alignment_scores:rate"]],
        ],
        axis=1,
    )

    Key_data = Key_data.rename({'ion_identities:ion_identities': "Adduct",
                    'spectral_db_matches:compound_name': "MS2 match",
                     'spectral_db_matches:cosine_score': "MS2 cosine score",
                     'compound_db_identity:compound_name': "MS1 match",
                     'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                     'formulas:formulas': 'Predicted MF',
                     'formulas:combined_score': 'MF score',
                     'alignment_scores:rate': "Alignment score"
                     }, axis='columns')

    PT_output = pd.ExcelWriter(
        "Final_Peak_Table_" + batch_name + ".xlsx", engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")
    (module_tables[3]).to_excel(PT_output, "Aligned_Feature_Data")
    (module_tables[1]).to_excel(PT_output, "MS2_Matching")
    (module_tables[0]).to_excel(PT_output, "MS1_Matching")
    (module_tables[2]).to_excel(PT_output, "MF_Prediction")
    (module_tables[4]).to_excel(PT_output, "IIN_Data")
    all_stats.to_excel(PT_output, "All_Stats")
    heights.to_excel(PT_output, "Raw Peak Heights")

    PT_output.close()

def export_fraction_PT(fraction_mods_filt: list, fraction_stats: pd.DataFrame, fraction_FC: pd.Series, g):

    Key_data = pd.concat([(fraction_mods_filt[7])[["Level_of_ID", "mz", "rt", "feature_group"]],
                          (fraction_mods_filt[4])[["ion_identities:ion_identities"]],
                          (fraction_mods_filt[1])[["spectral_db_matches:compound_name", "spectral_db_matches:cosine_score"]],
                          (fraction_mods_filt[0])[["compound_db_identity:compound_name", "compound_db_identity:mz_diff_ppm"]],
                          (fraction_mods_filt[2])[["formulas:formulas", "formulas:combined_score"]],
                          (fraction_mods_filt[3])[["alignment_scores:rate"]],
                           fraction_stats,
                           pd.Series(fraction_FC)],
                           axis=1,)

    Key_data = Key_data.rename({'ion_identities:ion_identities': "Adduct",
                                'spectral_db_matches:compound_name': "MS2 match",
                                'spectral_db_matches:cosine_score': "MS2 cosine score",
                                'compound_db_identity:compound_name': "MS1 match",
                                'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                                'formulas:formulas': 'Predicted MF',
                                'formulas:combined_score': 'MF score',
                                'alignment_scores:rate': "Alignment score"
                                }, axis='columns')

    mapping = {Key_data.columns[12]: 'RSD', Key_data.columns[13]: 'SD', Key_data.columns[14]: 'Avg Height', Key_data.columns[15]: 'FC'}
    Key_data = Key_data.rename(columns=mapping)

    Key_data = Key_data.sort_values(by = ['Avg Height'], ascending=False)

    PT_output = pd.ExcelWriter(
        g + "Peak_Table" + ".xlsx", engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")

    PT_output.close()

def export_blank_PT(fraction_mods_filt: list, fraction_stats: pd.DataFrame):


    Key_data = pd.concat([(fraction_mods_filt[7])[["mz", "rt", "feature_group"]],
                          (fraction_mods_filt[4])[["ion_identities:ion_identities"]],
                          (fraction_mods_filt[1])[["spectral_db_matches:compound_name", "spectral_db_matches:cosine_score"]],
                          (fraction_mods_filt[0])[["compound_db_identity:compound_name", "compound_db_identity:mz_diff_ppm"]],
                          (fraction_mods_filt[2])[["formulas:formulas", "formulas:combined_score"]],
                          (fraction_mods_filt[3])[["alignment_scores:rate"]],
                           fraction_stats],
                           axis=1,)


    Key_data = Key_data.rename({'ion_identities:ion_identities': "Adduct",
                                'spectral_db_matches:compound_name': "MS2 match",
                                'spectral_db_matches:cosine_score': "MS2 cosine score",
                                'compound_db_identity:compound_name': "MS1 match",
                                'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                                'formulas:formulas': 'Predicted MF',
                                'formulas:combined_score': 'MF score',
                                'alignment_scores:rate': "Alignment score"
                                }, axis='columns')

    mapping = {Key_data.columns[11]: 'RSD', Key_data.columns[12]: 'SD', Key_data.columns[13]: 'Avg Height'}
    Key_data = Key_data.rename(columns=mapping)

    Key_data = Key_data.sort_values(by = ['Avg Height'], ascending=False)

    date = datetime.datetime.now()

    Key_data["Date/Time"] = date

    PT_output = pd.ExcelWriter(
        ("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Bactobio_LCMS_Database/" + (str(date)[0:10]) + "_Bactobio_Blank_DB" + ".xlsx"), engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")

    PT_output.close()


def export_group_PT_forDB(fraction_mods_filt: list, fraction_stats: pd.DataFrame, g):


    Key_data = pd.concat([(fraction_mods_filt[7])[["mz", "rt", "feature_group"]],
                          (fraction_mods_filt[4])[["ion_identities:ion_identities"]],
                          (fraction_mods_filt[1])[["spectral_db_matches:compound_name", "spectral_db_matches:cosine_score"]],
                          (fraction_mods_filt[0])[["compound_db_identity:compound_name", "compound_db_identity:mz_diff_ppm"]],
                          (fraction_mods_filt[2])[["formulas:formulas", "formulas:combined_score"]],
                          (fraction_mods_filt[3])[["alignment_scores:rate"]],
                           fraction_stats],
                           axis=1,)


    Key_data = Key_data.rename({'ion_identities:ion_identities': "Adduct",
                                'spectral_db_matches:compound_name': "MS2 match",
                                'spectral_db_matches:cosine_score': "MS2 cosine score",
                                'compound_db_identity:compound_name': "MS1 match",
                                'compound_db_identity:mz_diff_ppm': "MS1 ppm error",
                                'formulas:formulas': 'Predicted MF',
                                'formulas:combined_score': 'MF score',
                                'alignment_scores:rate': "Alignment score"
                                }, axis='columns')

    mapping = {Key_data.columns[11]: 'RSD', Key_data.columns[12]: 'SD', Key_data.columns[13]: 'Avg Height'}
    Key_data = Key_data.rename(columns=mapping)

    Key_data = Key_data.sort_values(by = ['Avg Height'], ascending=False)

    date = datetime.datetime.now()

    Key_data["Date/Time"] = date

    PT_output = pd.ExcelWriter(
        ("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Bactobio_LCMS_Database/" + g + "Peak_Table" + ".xlsx"), engine="openpyxl", mode="w"
    )

    Key_data.to_excel(PT_output, "Key_Data")

    PT_output.close()
