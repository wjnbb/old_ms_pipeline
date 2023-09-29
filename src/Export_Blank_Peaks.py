import pandas as pd
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Export_Peak_Table import export_blank_PT
from src.assign_global_variables import RSD_threshold

def export_blank_peaks(blank_stats: pd.DataFrame, blank_db_filt : list, mods: list):

    print("")
    print("RSD threshold applied is " + str(RSD_threshold))
    print("")

    blank_rsd_peaks = list()

    #check each peak/row in the dataframe for minimum RSD threhsold
    for i in blank_stats.index:

        if blank_stats.loc[i,("Blank_rsd")] <= RSD_threshold:

            #add the peak row index where the minimum conditions were met
            blank_rsd_peaks.append(i)

    #check which of the blank peaks identifed during blank filtering have acceptable rproducibility for addition to the DB
    blank_peaks = [x for x in blank_db_filt if x in blank_rsd_peaks]

    #filter the mzmine modules and other tables by the remaining indices
    blank_db_mods_filt = module_tables_filt(blank_peaks, mods)
    blank_stats = single_table_filt(blank_peaks, blank_stats)

    print(str(len(blank_peaks)) + " peaks of blank origin were added to the Bactobio Blanks DB ")

    export_blank_PT(blank_db_mods_filt, blank_stats)