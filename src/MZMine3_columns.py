def mzmine3_cols(peak_table):

    # get all column names to allow subsequent organisation of samples names and table subsections

    pt_cols = list(peak_table.columns)
    print(pt_cols[0:10])
    return pt_cols
