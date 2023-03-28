import pandas as pd


def single_table_filt(filt_indices, df):

    filt_df = df.loc[
        filt_indices,
    ]

    return filt_df


def module_tables_filt(
    filt_indices: list, module_tables: tuple[pd.DataFrame]
) -> list[pd.DataFrame]:

    module_table_filt = list()

    for m in module_tables:

        mod_filt = m.loc[
            filt_indices,
        ]
        module_table_filt.append(mod_filt)

    return module_table_filt
