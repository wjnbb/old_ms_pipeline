import pandas as pd


def divide_mzmine3_table(peak_table: pd.DataFrame, pt_cols: list):

    """Takes a list of MZMine3 column names and uses the consistent prefixes for the different processing modules to
    divide it into a separate dataframe for each processing module applied as well as a peak height matrix."""

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
    fwhm_df = sample_data[(s for s in sample_cols if s.endswith(":fwhm"))]
    asymmetry_df = sample_data[(s for s in sample_cols if s.endswith(":asymmetry_factor"))]
    tailing_df = sample_data[(s for s in sample_cols if s.endswith(":tailing_factor"))]
    charge_df = sample_data[(s for s in sample_cols if s.endswith(":charge"))]
    isotopes_df = sample_data[(s for s in sample_cols if s.endswith(":isotopes"))]
    area_df = sample_data[(s for s in sample_cols if s.endswith(":area"))]
    frag_scans_df = sample_data[(s for s in sample_cols if s.endswith(":fragment_scans"))]
    ms2_apex_dist_df = sample_data[(s for s in sample_cols if s.endswith(":rt_ms2_apex_distance"))]

    print("\ncompleted MZMine3 peak table dividing")

    return (
        MS1_match_data,
        MS2_match_data,
        MF_pred_data,
        Alignment_data,
        IIN_data,
        manual_anno_data,
        height_df,
        aligned_feature_info,
        fwhm_df,
        asymmetry_df,
        tailing_df,
        charge_df,
        isotopes_df,
        area_df,
        frag_scans_df,
        ms2_apex_dist_df
    )
