import os
import pandas as pd
import numpy as np
from src.Standards import (chloramphenicol,
                           cycloheximide,
                           hygromycin,
                           imipenem,
                           neomycin,
                           nystatin,
                           polymyxin_b,
                           tetracycline,
                           fosfomycin,
                           lincomycin,
                           paromomycin,
                           penicillin_g,
                           rifampicin,
                           vancomycin,
                           tobramycin,
                           thiostrepton)

def feature_group_summariser(batch_subfolder):

    standards = [chloramphenicol,
                 cycloheximide,
                 hygromycin,
                 imipenem,
                 neomycin,
                 nystatin,
                 polymyxin_b,
                 tetracycline,
                 fosfomycin,
                 lincomycin,
                 paromomycin,
                 penicillin_g,
                 rifampicin,
                 vancomycin,
                 tobramycin,
                 thiostrepton]

    #batch_subfolder = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20240109_Set1and2mix_LM2/MZMine3"

    os.chdir(batch_subfolder)

    #read in the necessary csv from the batch subfolder
    feature_groups = pd.read_csv("Feature_groups.csv",
                                 usecols=[1, 2],
                                 index_col=0)

    feature_group_stats = pd.read_csv("Feature_Group_Stats.csv",
                                 usecols=[1, 2, 3, 4, 5, 6],
                                 index_col=0)
    feature_group_stats = feature_group_stats.drop(columns=["Experimental_m/z",
                                                            "Matched_Adduct"],
                                                   axis=1)

    lorcd = pd.read_csv("LORCD.csv",
                                 usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                 index_col=0)

    lorcd_fg_filt = pd.read_csv("LORCD_filtered_outputs.csv",
                                 usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                 index_col=0)
    lorcd_fg_filt.replace(0,np.nan, inplace=True)

    # get total number of unique feature groups
    unique_fg_total = len(np.unique(feature_groups["Feature_Group"]))
    # get total number of ungrouped major/protonated ion features
    nan_groups_total = (feature_groups["Feature_Group"]).isna().sum()
    # get the average feature group size for major/protonated ion feature groups in the dataset
    avg_fg_size_total = (feature_group_stats.drop_duplicates()["Feature_Group_Size"]).mean()
    # get the average fg accuracy for the major/protonated ion feature groups in the dataset
    avg_fg_accuracy_total = (feature_group_stats.drop_duplicates()["FG_match_percentages"]).mean()
    # get the number of feature groups which contain major/protonated ions from more than one standard
    fg_counts = feature_groups.value_counts()
    multi_standard_fgs = len(fg_counts[fg_counts >= 2])

    #seed
    standard_unique_groups = []
    standard_nan_groups = []
    standard_avg_fg_size = []
    standard_avg_fg_accuracy = []
    standard_lorcd_values = []
    standard_lorcd_fg_filt_values = []


    for standard in standards:

        # check if the standard was found first to avoid error
        if standard["name"] in feature_groups.index:

            # get the number of unique feature groups for the current standard
            standard_unique_groups.append(len(feature_groups.loc[standard["name"]]))
            # get the average feature group size and accuracy for the current standard
            standard_fg_stats = (feature_group_stats.loc[standard["name"]]).drop_duplicates()
            standard_avg_fg_size.append((standard_fg_stats["Feature_Group_Size"]).mean())
            standard_avg_fg_accuracy.append((standard_fg_stats["FG_match_percentages"]).mean())

            # if statement required here for code to work as desired for standards with more than one row of data
            if len(feature_groups.loc[standard["name"]]) > 1:

                # get the number of major/protonated ions not assigned a feature group for the current standard
                standard_nan_groups.append(((feature_groups.loc[standard["name"]]).isnull().sum()).iloc[0])

            else:

                # get the number of major/protonated ions not assigned a feature group for the current standard
                standard_nan_groups.append(((feature_groups.loc[standard["name"]]).isnull().sum()))


            # #get the LORCD_filtered_output comparison to the LORCD output
            conc_values = [400, 200, 100, 50, 25, 12.5, 6.25, 3.125, 1.5625, 0.78125, 0.390625]
            conc_cols = list(reversed(lorcd.columns.values))


            #loop through the columns in order from lowest to highest concentration
            for col in conc_cols:

                #subset the lorcd data by the standard name
                standard_lorcd = lorcd.loc[standard["name"]]
                #conc_col = standard_lorcd[[col]]

                #check if the column is all missing values or not for this concentration
                if ((standard_lorcd[[col]]).isna().all().all()) == False:

                    #numeric values were found in this concentration column (True LORCD found)
                    #print(f"True LORCD for {standard['name']} is {col}")

                    #check the fg filtered LORCD table to see if results align or if FG filtering is removing it
                    standard_lorcd_fg_filt = lorcd_fg_filt.loc[standard["name"]]
                    fg_filt_conc_col = standard_lorcd_fg_filt[[col]]
                    standard_lorcd_values.append([col, standard['name']])

                    #check if the column is all missing values or not for this concentration
                    if fg_filt_conc_col.isna().all().all() == False:

                        #numeric values found in thic conentration col
                        #print(f"FG filtering is true to the true LORCD for {standard['name']}")
                        standard_lorcd_fg_filt_values.append([col, standard['name']])
                        break

                    else:
                        #print("FG filtering is NOT true to LORCD")

                        #get the remaining conc columns in their own df
                        remaining_conc_cols = conc_cols[((conc_cols.index(col))+1):]

                        # loop through the remaining concentration cols
                        for rcol in remaining_conc_cols:

                            #subset the df to leave just the conc column for the standard in question
                            fg_filt_conc_col = standard_lorcd_fg_filt[[rcol]]

                            # check if the column contains any numeric data
                            if fg_filt_conc_col.isna().all().all() == False:

                                # numeric data is found
                                #print(f"FG filtering is true to the true LORCD for {standard['name']}")
                                standard_lorcd_fg_filt_values.append([rcol, standard['name']])
                                break

                            else:
                                continue


                else:

                    if col == '400 ug/mL':

                        #print("made it to last concentration without breaking the loop")
                        standard_lorcd_values.append("Not in outputs")
                        standard_lorcd_fg_filt_values.append("Not in outputs")

        else:

            # append zeros for cases where the if statement wasn't satisfied
            standard_unique_groups.append(0)
            standard_nan_groups.append(0)
            standard_avg_fg_size.append(0)
            standard_avg_fg_accuracy.append(0)
            standard_lorcd_values.append(["Not in outputs", standard["name"]])
            standard_lorcd_fg_filt_values.append(["Not in outputs", standard["name"]])


    standard_lorcd_values = pd.DataFrame(standard_lorcd_values)
    standard_lorcd_values.columns = ["LORCD ug/mL", "Standard1"]
    standard_lorcd_values["LORCD ug/mL"] = standard_lorcd_values["LORCD ug/mL"].str.replace(" ug/mL", "")
    standard_lorcd_fg_filt_values = pd.DataFrame(standard_lorcd_fg_filt_values)
    standard_lorcd_fg_filt_values.columns = ["FG_Filt_LORCD ug/mL", "Standard2"]
    standard_lorcd_fg_filt_values["FG_Filt_LORCD ug/mL"] = standard_lorcd_fg_filt_values["FG_Filt_LORCD ug/mL"].str.replace(" ug/mL", "")

    final_standard_lorcd_values = pd.DataFrame()
    final_standard_lorcd_fg_filt_values = pd.DataFrame()

    #organise lorcd fg filt values into right format for concatenatuin to other gathered data
    for standard in standards:

        sfilt = standard_lorcd_values.loc[standard_lorcd_values["Standard1"] == standard["name"]]

        final_standard_lorcd_values = pd.concat(
                                                [final_standard_lorcd_values,
                                                (sfilt[sfilt["LORCD ug/mL"]==sfilt["LORCD ug/mL"].min()])],
                                                 axis=0
        )

        sfgfilt = standard_lorcd_fg_filt_values.loc[standard_lorcd_fg_filt_values["Standard2"] == standard["name"]]

        final_standard_lorcd_fg_filt_values = pd.concat(
            [final_standard_lorcd_fg_filt_values,
             (sfgfilt[sfgfilt["FG_Filt_LORCD ug/mL"] == sfgfilt["FG_Filt_LORCD ug/mL"].min()])],
            axis=0
        )

    # formatting output from above loop ready for concatenation
    final_standard_lorcd_fg_filt_values.drop_duplicates(inplace=True)
    final_standard_lorcd_fg_filt_values.reset_index(inplace=True)
    final_standard_lorcd_values.reset_index(inplace=True)

    #concatenate all key data ready for export
    result_df = pd.concat([
                           final_standard_lorcd_values,
                           final_standard_lorcd_fg_filt_values,
                           pd.Series(standard_unique_groups, name="Unique FG Count"),
                           pd.Series(standard_nan_groups, name="Ungrouped Major/Protonated Ion Count"),
                           pd.Series(standard_avg_fg_size, name="Average FG Size"),
                           pd.Series(standard_avg_fg_accuracy, name="Average FG Accuracy")
                           ],
                           axis=1
    )

    #tidy up df ready for export and export
    result_df = result_df.drop(columns="index")
    result_df = result_df.drop("Standard2", axis=1)
    result_df = result_df.set_index(list(result_df[["Standard1"]]))
    result_df.to_csv(f"{batch_subfolder}/FG_summary_standards.csv")

    #get the numebr of standards for which LORCD is less than FGfilt LORCD
    FG_filt_incorrect_count = 0
    for standard in standards:

        #skip fosfomycin as it is undetected and has a string value causing errors
        if standard == fosfomycin:
            continue

        # logical statement to check LORCD is lower than FGfilt LORCD
        elif float((result_df[["LORCD ug/mL"]]).loc[standard["name"]]) < float((result_df[["FG_Filt_LORCD ug/mL"]]).loc[standard["name"]]):

            FG_filt_incorrect_count = FG_filt_incorrect_count + 1


    #combine info for the dataset as a whole ready for export
    dataset_summary = pd.DataFrame([unique_fg_total,
                       nan_groups_total,
                       avg_fg_size_total,
                       avg_fg_accuracy_total,
                       multi_standard_fgs,
                       FG_filt_incorrect_count
                       ],
                       index=["Unique FG Count",
                      "Nan Count",
                      "Average FG Size",
                      "Average FG Accuracy %",
                      "Multi-standard FG Counts",
                      "FG filter incorrect count"]
                      )

    print(f"Printing batch subfolder {batch_subfolder}")

    dataset_summary.to_csv(f"{batch_subfolder}/FG_summary_dataset.csv")














