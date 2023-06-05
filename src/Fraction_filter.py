import pandas as pd
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Export_Peak_Table import export_fraction_PT
from src.assign_global_variables import bio_media_linkers, Bio_identifier, FC_threshold, RSD_threshold, peak_height_threshold


def fraction_filter(Bio_stats: pd.DataFrame, active_groups: list, FC_Stats: pd.DataFrame, Mods_filt: list[pd.DataFrame]):

    #Check if bio_media_linkers were applied or not
    if(bio_media_linkers != "NA"):

        #loop through the biological sample groups in the dataset
        for g in active_groups:

            #check that the current biological sample group in question found in bio_media_linkers, if not skip it
            if any(b in g for b in bio_media_linkers):

                fraction_peaks = list()

                #check each peak/row in the dataframe for minium RSD, peak height and FC threshold
                for i in Bio_stats.index:

                    if(Bio_stats.loc[i,(g+"rsd")] <= RSD_threshold) &\
                      (Bio_stats.loc[i,(g+"avg")] >= peak_height_threshold) &\
                      (FC_Stats.loc[i,("FC"+g.split(Bio_identifier)[1])] >= FC_threshold):

                        #add the peak row index where the minimum conditions were met
                        fraction_peaks.append(i)

                #filter the mzmine modules and other tables by the remaining indices
                fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
                fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)
                fraction_FC = single_table_filt(fraction_peaks, FC_Stats)

                fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]
                fraction_FC = fraction_FC[[s for s in fraction_FC.columns if g.split(Bio_identifier)[1] in s]].squeeze()

                export_fraction_PT(fraction_mods_filt, fraction_FC, fraction_stats, g)

            else:

                continue

    else:

        for g in active_groups:

            fraction_peaks = list()

            for i in Bio_stats.index:

                if (Bio_stats.loc[i, (g + "rsd")] <= RSD_threshold) & \
                        (Bio_stats.loc[i, (g + "avg")] >= peak_height_threshold) & \
                        (FC_Stats.loc[i, ("FC" + g.split(Bio_identifier)[1])] >= FC_threshold):

                    fraction_peaks.append(i)


            fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
            fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)
            fraction_FC = single_table_filt(fraction_peaks, FC_Stats)

            fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]
            fraction_FC = fraction_FC[[s for s in fraction_FC.columns if g in s]].squeeze()

            export_fraction_PT(fraction_mods_filt, fraction_FC, fraction_stats, g)

