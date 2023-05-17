def get_sample_names(height_df):

    # Pattern match on column names in the peak height data frame
    # take everything after datafile: to get the sample names

    sample_names_full = [name.split(":")[1] for name in height_df.columns]
    sample_names = [name.split("-")[1] for name in sample_names_full]

    return sample_names
