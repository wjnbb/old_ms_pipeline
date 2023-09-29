import pandas as pd
import numpy as np

def transformation_multi(norm_heights: tuple[pd.DataFrame], trans_type: str):

    """Transforms all average peak height columns in tuple of dataframes supplied. Use either "log", "log10" or "log2"
     to specify the transformation type. Returns a list of transformed dataframes."""

    norm_heights = list(norm_heights)
    trans_heights = list()

    for df in norm_heights:

        if trans_type == "log":

            df = df.apply(np.log)
            trans_heights.append(df)

        elif trans_type == "log10":

            df = df.apply(np.log10)
            trans_heights.append(df)

        elif trans_type == "log2":

            df = df.apply(np.log2)
            trans_heights.append(df)

    return trans_heights

def transformation_single(df: pd.DataFrame, trans_type: str):

    """Transforms all average peak height columns in the supplied dataframe. Use either "log", "log10" or "log2"
     to specify the transformation type. Returns a transformed dataframe."""

    if len([s for s in df.columns if "avg" in s]) != 0:

        df = df[[s for s in df.columns if "avg" in s]]

    if trans_type == "log":

        df = df.apply(np.log)

    elif trans_type == "log10":

        df = df.apply(np.log10)

    elif trans_type == "log2":

        df = df.apply(np.log2)

    return df


