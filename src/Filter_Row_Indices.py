import pandas as pd


def single_table_filt(filt_indices: list, df: pd.DataFrame) -> pd.DataFrame:

    """Takes a list of row indices to filter out the relevant rows and a Pandas dataframe of the peak height stats for
    the group in question. Returns a filtered pandas dataframe of peak height stats."""

    if df.empty:
        filt_df = pd.DataFrame()
        return filt_df

    filt_df = df.loc[
        filt_indices,
    ]

    return filt_df


def module_tables_filt(
    filt_indices: list, module_tables: tuple[pd.DataFrame]
) -> list[pd.DataFrame]:

    """Takes a list of row indices and a tuple of Pandas dataframes and filters by row using the indices for each
    dataframe within the tuple. Returns a tuple of row filtered Pandas dataframes."""

    module_table_filt = list()

    for m in module_tables:

        mod_filt = m.loc[
            filt_indices,
        ]
        module_table_filt.append(mod_filt)

    return module_table_filt
