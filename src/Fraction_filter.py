import numpy as np
import pandas as pd
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Export_Peak_Table import export_fraction_PT, export_group_PT_forDB, export_fraction_PT_noFC
from src.assign_global_variables import bio_media_linkers, Bio_identifier, RSD_threshold, FC_threshold, peak_height_threshold

def fraction_filter(Bio_stats: pd.DataFrame, active_groups: list, FC_Stats: pd.DataFrame, Mods_filt: list):

    print("")
    print("FC threshold applied is " + str(FC_threshold))
    print("RSD threshold applied is " + str(RSD_threshold))
    print("Peak height threshold applied is " + str(peak_height_threshold))
    print("")

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

                print(str(len(fraction_peaks)) + " features meet the filtering criteria in " + str(g))

                fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]
                fraction_FC = fraction_FC[[s for s in fraction_FC.columns if g.split(Bio_identifier)[1] in s]].squeeze()

                if not isinstance(fraction_FC, pd.Series):

                    fraction_FC = pd.Series(fraction_FC)

                export_fraction_PT(fraction_mods_filt, fraction_stats, fraction_FC, g)

            else:

                continue

    else:

        for g in active_groups:

            fraction_peaks = list()

            for i in Bio_stats.index:

                if (Bio_stats.loc[i, (g + "rsd")] <= RSD_threshold) & \
                        (Bio_stats.loc[i, (g + "avg")] >= peak_height_threshold) & \
                        (FC_Stats.loc[i, ("FC_" + str(g))] >= FC_threshold):


                    fraction_peaks.append(i)


            fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
            fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)
            fraction_FC = single_table_filt(fraction_peaks, FC_Stats)

            print(str(len(fraction_peaks)) + " features meet the filtering criteria in " + str(g))

            fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]
            fraction_FC = fraction_FC[[s for s in fraction_FC.columns if g in s]].squeeze()

            if not isinstance(fraction_FC, pd.Series):

                fraction_FC = pd.Series(fraction_FC)

            export_fraction_PT(fraction_mods_filt, fraction_stats, fraction_FC, g)


def fraction_filter_noFC(
        Bio_stats: pd.DataFrame,
        active_groups: list,
        Mods_filt: list,
        peak_quality_metrics:pd.DataFrame
):

    for g in active_groups:

        fraction_peaks = list()

        for i in Bio_stats.index:

            if (Bio_stats.loc[i, (g + "_rsd")] <= RSD_threshold) & \
                (Bio_stats.loc[i, (g + "_avg")] >= peak_height_threshold) & \
                (peak_quality_metrics.loc[i, "Isotopes"] > 0) & \
                (peak_quality_metrics.loc[i, "Charge"] > 0) & \
                ((peak_quality_metrics.loc[i, "Number of Aligned Features"]) +
                 (peak_quality_metrics.loc[i, "Align Extra Features Number"]) >= 3):


                peak_check_count = 0

                if 0.05 <= peak_quality_metrics.loc[i, "FWHM"] <= 0.2:
                    peak_check_count = peak_check_count + 1
                if 0.5 <= peak_quality_metrics.loc[i, "asymmetry_factor"] <= 3.0:
                    peak_check_count = peak_check_count + 1
                if 0.5 <= peak_quality_metrics.loc[i, "tailing_factor"] <= 3.0:
                    peak_check_count = peak_check_count + 1
                if 0.75 <= peak_quality_metrics.loc[i, "Weighted Distance Score"] < 1.0:
                    peak_check_count = peak_check_count + 1

                if peak_check_count >= 2:
                    #print(f"peak id {i} passes filtering criteria")
                    fraction_peaks.append(i)

            else:
                continue


        fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
        fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)

        print("")
        print(str(len(fraction_peaks)) + " features meet the peak quality filtering criteria in " + str(g))

        #get summary peak info for further filtering to make output simpler, only report 1 feature per feature group
        peak_info = fraction_mods_filt[7]

        #get adduct info
        adduct_info = fraction_mods_filt[4]
        adducts = adduct_info["ion_identities:ion_identities"]

        #getms2 match info
        ms2_info = fraction_mods_filt[1]
        ms2_matches = ms2_info["spectral_db_matches:spectral_db_matches"]

        #add the adduct and ms2 info to the peak info
        peak_info = peak_info.merge(adducts, left_index = True, right_index = True)
        peak_info = peak_info.merge(ms2_matches, left_index = True, right_index = True)

        #get unique feature groups
        feature_groups = peak_info.feature_group.unique()

        #print(f"There are {len(feature_groups)} unique feature groups (metabolites) in the output for {g}")

        filtered_features = []
        feature_group_size = []

        for fg in feature_groups:

            #subset the table for the feature group
            feature_group_info = peak_info[peak_info["feature_group"] == fg]
            #print(f"There are {len(feature_group_info)} features in the feature group {fg}")

            for feature in feature_group_info.index:

                if ((feature_group_info.loc[feature, "ion_identities:ion_identities"] == "[M+H]+") |
                        (feature_group_info.loc[feature, "ion_identities:ion_identities"] == "[M+Na]+") |
                        (feature_group_info.loc[feature, "ion_identities:ion_identities"] == "[M+2H]2+")):

                    filtered_features.append(feature)
                    feature_group_size.append(len(feature_group_info))

                elif pd.isna(feature_group_info.loc[feature, "spectral_db_matches:spectral_db_matches"]) == False:

                    filtered_features.append(feature)
                    feature_group_size.append(len(feature_group_info))

                elif feature_group_info.loc[feature, "height"] == np.max(feature_group_info.height):

                    filtered_features.append(feature)
                    feature_group_size.append(len(feature_group_info))

        print(f"{len(filtered_features)} features meet the feature group filtering criteria in {g}")

        feature_group_size = pd.Series(feature_group_size)

        fraction_stats = single_table_filt(filtered_features, Bio_stats)
        fraction_mods_filt = module_tables_filt(filtered_features, Mods_filt)
        feature_group_size = feature_group_size.set_axis(fraction_stats.index)
        fr_peak_quality_metrics = single_table_filt(filtered_features, peak_quality_metrics)

        fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]
        export_fraction_PT_noFC(fraction_mods_filt, fraction_stats, g, feature_group_size, fr_peak_quality_metrics)


def db_filter(Bio_stats: pd.DataFrame, active_groups: list, Mods_filt: list):

    print("")
    print("RSD threshold applied is " + str(RSD_threshold))
    print("Peak height threshold applied is " + str(peak_height_threshold))
    print("")

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
                      (Bio_stats.loc[i,(g+"avg")] >= peak_height_threshold):

                        #add the peak row index where the minimum conditions were met
                        fraction_peaks.append(i)


                #filter the mzmine modules and other tables by the remaining indices
                fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
                fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)

                print(str(len(fraction_peaks)) + " features meet the filtering criteria in " + str(g))

                fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]

                export_group_PT_forDB(fraction_mods_filt, fraction_stats, g)

            else:

                continue

    else:

        for g in active_groups:

            fraction_peaks = list()

            for i in Bio_stats.index:

                if (Bio_stats.loc[i, (g + "rsd")] <= RSD_threshold) & \
                        (Bio_stats.loc[i, (g + "avg")] >= peak_height_threshold):

                    fraction_peaks.append(i)

            fraction_stats = single_table_filt(fraction_peaks, Bio_stats)
            fraction_mods_filt = module_tables_filt(fraction_peaks, Mods_filt)

            print(str(len(fraction_peaks)) + " features meet the filtering criteria and were added to the Bactobio LC-MS database for the sample " + str(g) )

            fraction_stats = fraction_stats[[s for s in fraction_stats.columns if g in s]]

            export_group_PT_forDB(fraction_mods_filt, fraction_stats, g)
