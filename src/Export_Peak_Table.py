import pandas as pd

from src.assign_global_variables import batch_name


def export_PT_w_norm(
    module_tables: list[pd.DataFrame],
    FC_Stats: pd.DataFrame,
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
    group_heights: tuple[pd.DataFrame],
    norm_heights: tuple[pd.DataFrame],
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
            ((module_tables[7])[["mz", "rt", "feature_group"]]),
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


def export_PT(
    module_tables: list[pd.DataFrame],
    FC_Stats: pd.DataFrame,
    Bio_stats: pd.DataFrame,
    Media_stats: pd.DataFrame,
    QC_stats: pd.DataFrame,
    Blank_stats: pd.DataFrame,
    group_heights: tuple[pd.DataFrame]
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
            ((module_tables[7])[["mz", "rt", "feature_group"]]),
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

    PT_output.save()

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
            ((module_tables[7])[["mz", "rt", "feature_group"]]),
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

    PT_output.save()


