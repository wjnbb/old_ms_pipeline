import pandas as pd


def rt_filter(peak_info: pd.DataFrame, RT_min: float, RT_max: float):
    """Takes the peak info and checks the RT column for features that fall within the min and max expected RT."""

    rt_filt = list()
    print("\nMinimum RT for filtering was " + str(RT_min))
    print("Maximum RT for filtering was " + str(RT_max))

    for i in peak_info.index:

        if (peak_info.loc[i, "rt"] >= RT_min) & (peak_info.loc[i, "rt"] <= RT_max):

            rt_filt.append(i)

    print(str(len(rt_filt)) + " features left after RT filtering.")

    return rt_filt
