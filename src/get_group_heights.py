def get_group_heights(height_df, Bio, Media, Blanks, QCs):

    Bio_table = height_df.loc[
        :, [c for c in height_df.columns if any(b in c for b in Bio)]
    ]
    Media_table = height_df.loc[
        :, [c for c in height_df.columns if any(m in c for m in Media)]
    ]
    Blank_table = height_df.loc[
        :, [c for c in height_df.columns if any(b in c for b in Blanks)]
    ]
    QC_table = height_df.loc[
        :, [c for c in height_df.columns if any(q in c for q in QCs)]
    ]

    return Bio_table, Media_table, Blank_table, QC_table
