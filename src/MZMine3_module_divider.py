import pandas as pd


def divide_mzmine3_table(peak_table, pt_cols):

    # divide different sections of mzmine3 table into the processing modules they originate from by matching the prefix in the column headers
    # Get the aligned feature info into one data frame
    aligned_feature_info = peak_table[(c for c in pt_cols if ":" not in c)]
    rt_range_cols = peak_table[(c for c in pt_cols if c.startswith("rt_range:"))]
    mz_range_cols = peak_table[(c for c in pt_cols if c.startswith("mz_range:"))]
    intensity_range_cols = peak_table[
        (c for c in pt_cols if c.startswith("intensity_range:"))
    ]
    aligned_feature_info = pd.concat(
        [aligned_feature_info, rt_range_cols, mz_range_cols, intensity_range_cols],
        axis=1,
    )

    # get all sample specific data into one data frame
    sample_data = peak_table[(c for c in pt_cols if c.startswith("datafile:"))]

    # Organise data in different data frame based on annotation module origin
    MS1_match_data = peak_table[
        (c for c in pt_cols if c.startswith("compound_db_identity:"))
    ]
    MS2_match_data = peak_table[
        (c for c in pt_cols if c.startswith("spectral_db_matches:"))
    ]
    MF_pred_data = peak_table[(c for c in pt_cols if c.startswith("formulas:"))]
    Alignment_data = peak_table[
        (c for c in pt_cols if c.startswith("alignment_scores:"))
    ]
    IIN_data = peak_table[(c for c in pt_cols if c.startswith("ion_identities:"))]
    manual_anno_data = peak_table[
        (c for c in pt_cols if c.startswith("manual_annotation:"))
    ]
    # Loop through the sample cols to get the peak height for each sample to make peak matrix
    sample_cols = list(sample_data.columns)
    height_df = sample_data[(s for s in sample_cols if s.endswith(":height"))]

    print("completed MZMine3 peak table dividing")

    return (
        MS1_match_data,
        MS2_match_data,
        MF_pred_data,
        Alignment_data,
        IIN_data,
        manual_anno_data,
        height_df,
        aligned_feature_info,
    )
