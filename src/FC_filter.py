import pandas as pd
from src.assign_global_variables import FC_threshold, RT_min, RT_max

def FC_filter(FC_Stats: pd.DataFrame):

    """Finds the indices of all rows in the supplied dataframe of FC data that meet the minimum FC threshold in at
    least one column in that row."""

    FC_filt = list()
    print("")
    print("FC threshold applied was " + str(FC_threshold))

    #search each row of the FC data to find all rows where the max FC is greater than the FC_threshold applied
    for i in FC_Stats.index:

        if len((FC_Stats.loc[i, :]).dropna()) == 0:

            continue

        elif(max((FC_Stats.loc[i, :]).dropna())) >= FC_threshold:

            FC_filt.append(i)

    print(str((len(FC_Stats))-len(FC_filt)) + " features were removed for not meeting the minimum FC threshold")
    print(str(len(FC_filt)) + " features remain after FC filtering")

    return FC_filt
