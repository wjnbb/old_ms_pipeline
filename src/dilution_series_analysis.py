#from src.feature_group_checker import feature_group_checker
# from src.Standards import (chloramphenicol,
#                            cycloheximide,
#                            hygromycin,
#                            imipenem,
#                            neomycin,
#                            nystatin,
#                            polymyxin_b,
#                            tetracycline)
#
#
# #make list of standards dictionary entries
# standards = [chloramphenicol,
#              cycloheximide,
#              hygromycin,
#              imipenem,
#              neomycin,
#              nystatin,
#              polymyxin_b,
#              tetracycline
#              ]


# from src.Standards import (fosfomycin,
#                            lincomycin,
#                            paromomycin,
#                            penicillin_g,
#                            rifampicin,
#                            vancomycin,
#                            tobramycin,
#                            thiostrepton)
#
# standards = [fosfomycin,
#              lincomycin,
#              paromomycin,
#              penicillin_g,
#              rifampicin,
#              vancomycin,
#              tobramycin,
#              thiostrepton]

from src.Standards import (chloramphenicol,
                           cycloheximide,
                           hygromycin,
                           imipenem,
                           neomycin,
                           nystatin,
                           polymyxin_b,
                           polymyxin_b2,
                           polymyxin_b6,
                           tetracycline,
                           anhydrotetracycline,
                           oxytetracycline,
                           fosfomycin,
                           lincomycin,
                           paromomycin,
                           penicillin_g,
                           rifampicin,
                           vancomycin,
                           tobramycin,
                           thiostrepton)

# standards = [chloramphenicol,
#              cycloheximide,
#              hygromycin,
#              imipenem,
#              neomycin,
#              nystatin,
#              polymyxin_b,
#              polymyxin_b2,
#              polymyxin_b6,
#              tetracycline,
#              anhydrotetracycline,
#              oxytetracycline,
#              fosfomycin,
#              lincomycin,
#              paromomycin,
#              penicillin_g,
#              rifampicin,
#              vancomycin,
#              tobramycin,
#              thiostrepton]

# from src.Standards import paromomycin
# standards = [paromomycin]

import pandas as pd
import os
import numpy as np
import plotly.express as px
from src.assign_global_variables import path
from src.ppm_calculator import ppm_calculator
from src.feature_group_checker import feature_group_checker
from src.plot_peak_quality import (
    plot_standards_fwhm,
    plot_standards_asymmetry,
    plot_standards_tailing,
    plot_standards_isotopes,
    plot_standards_charge,
    plot_standards_frag_scans,
    plot_standards_ms2_apex_dist,
    plot_standards_area,
    plot_standards_height
)
import os

def dil_series_analyser(standards, ppm:int, bio_stats):

    print(f"Printing the current working directory for the dil_series_analyser().. {os.getcwd()}")

    #import the precalculated adduct masses for each standard
    standards_adducts = pd.read_csv("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/Standards_adducts_set1and2.csv",
                          index_col=0)
    #get list of peak tables to be analysed
    os.chdir(path)
    files = os.listdir(path)
    #get list of only dilution series files
    dilution_series_files = ([s for s in files if "mL_Peak_Table" in s])
    #get name of the complete peak table and read it in
    full_peak_table = ([s for s in files if "Final" in s])
    full_peak_table = pd.read_excel(full_peak_table[0],
                                    index_col=0)

    #seed objects for results storage
    major_ion_matches = pd.DataFrame()
    compounds = []
    adduct_matches = []
    molecular_formula_matches = []
    ms1_matches = []
    ms2_matches = []
    fg_names = []
    fg_list = []

    #loop through standards
    for s in standards:

        #get mz for the major ion for this
        major_ion_mz = standards_adducts.loc[s["major_ion"], s["name"]]
        print("")
        print(s["major_ion"])
        print(major_ion_mz)


        #find the protonated ion as well as the major ion if the major ion isn't the protonated one
        if(s["major_ion"] != "[M+H]+"):

            print(f"checking for major ion and protonated ion for {s['name']}")

            #find the protonated ion mass and calculate min and max ppm errors
            protonated_ion = standards_adducts.loc["[M+H]+", s["name"]]
            print(protonated_ion)
            protonated_error = ppm_calculator(protonated_ion, ppm)
            protonated_max = protonated_ion + protonated_error
            protonated_min = protonated_ion - protonated_error
            # find protonated ion mz in the full peak table
            protonated_ion_info = full_peak_table[(full_peak_table["mz"] >= protonated_min) &
                                                  (full_peak_table["mz"] <= protonated_max)]

            # calculate min and max values for the major ion and min and max ppm errors
            mz_error = ppm_calculator(major_ion_mz, ppm)
            mz_max = major_ion_mz + mz_error
            mz_min = major_ion_mz - mz_error
            # find major ion mz in the full peak table
            major_ion_info = full_peak_table[(full_peak_table["mz"] >= mz_min) &
                                             (full_peak_table["mz"] <= mz_max)]

            #if major and protonated ions are not found this standard skip to the next one
            if (((major_ion_info.empty) == True) & ((protonated_ion_info.empty) == True)):
                print(f"no {s['name']} ions found")
                continue

            #ions were found so combine into a table for checking annotation info and also store in the final results table
            else:
                unique_fgs = list(np.unique(major_ion_info["feature_group"]))
                fg_list.extend(unique_fgs)
                fg_name = list(np.repeat(s['name'], len(unique_fgs)))
                fg_names.extend(fg_name)

                major_ion_info = pd.concat([major_ion_info, protonated_ion_info], axis=0)
                print(f"Found {len(major_ion_info)} ions for {s['name']}")
                major_ion_matches = pd.concat([major_ion_matches, major_ion_info], axis=0)
                compounds.extend(list(np.repeat(s["name"], len(major_ion_info), axis=0)))

                # Check if annotation information is correct for each row that matched to an mz of interest
                for row in major_ion_info.index.values:

                    print(row)

                    adduct = major_ion_info.loc[row, "Adduct"]
                    molecular_formula = major_ion_info.loc[row, "Predicted MF"]
                    ms1_match = major_ion_info.loc[row, "MS1 match"]
                    ms1_ppm = major_ion_info.loc[row, "MS1 ppm error"]
                    ms2_match = major_ion_info.loc[row, "MS2 match"]
                    ms2_score = major_ion_info.loc[row, "MS2 cosine score"]

                    if (adduct == s["major_ion"]):
                        adduct_matches.append("Yes")

                    else:
                        adduct_matches.append(f"No {adduct}")

                    if (molecular_formula == s["molecular_formula"]):
                        molecular_formula_matches.append("Yes")

                    else:
                        molecular_formula_matches.append(f"No {molecular_formula}")

                    if (ms1_match is np.nan):

                        ms1_matches.append("No match")

                    elif (s["name"].upper() in ms1_match.upper()):
                        (ms1_matches.append(f"Yes (ppm = {ms1_ppm})"))

                    else:
                        ms1_matches.append(f"No {ms1_match} ppm = {ms1_ppm}")

                    if (ms2_match is np.nan):

                        ms2_matches.append("No match")

                    elif (s["name"].upper() in ms2_match.upper()):
                        (ms2_matches.append(f"Yes Score = {ms2_score}"))

                    else:
                        ms2_matches.append(f"No {ms2_match}")


        # for cases where the major ion is the protonated ion
        else:

            #print("Major ion is protonated, searching for protonated ion only")

            #calculate min and max values for mz of interest and desired ppm error
            mz_error = ppm_calculator(major_ion_mz, ppm)
            mz_max = major_ion_mz + mz_error
            mz_min = major_ion_mz - mz_error
            #find major ion mz in the full peak table
            #print(full_peak_table[(full_peak_table["mz"] >= mz_min) &
            #                      (full_peak_table["mz"] <= mz_max)])

            major_ion_info = full_peak_table[(full_peak_table["mz"] >= mz_min) &
                                            (full_peak_table["mz"] <= mz_max)]

            # no match found in the peak table for the major ion so skip to the next standard
            if(major_ion_info.empty):
                #print(f"Protonated ion not found for {s['name']}")
                continue

            # match is found and added to the results table
            else:
                unique_fgs = list(np.unique(major_ion_info["feature_group"]))
                fg_list.extend(unique_fgs)
                fg_name = list(np.repeat(s['name'], len(unique_fgs)))
                fg_names.extend(fg_name)

                major_ion_matches = pd.concat([major_ion_matches, major_ion_info], axis=0)
                #print(f"Found {len(major_ion_info)} ions for {s['name']}")
                compounds.extend(list(np.repeat(s["name"], len(major_ion_info), axis=0)))


            #Check if annotation information is correct for each row that matched to an mz of interest
            for row in major_ion_info.index.values:

                #print(row)

                adduct = major_ion_info.loc[row, "Adduct"]
                molecular_formula = major_ion_info.loc[row, "Predicted MF"]
                ms1_match = major_ion_info.loc[row, "MS1 match"]
                ms1_ppm = major_ion_info.loc[row, "MS1 ppm error"]
                ms2_match = major_ion_info.loc[row, "MS2 match"]
                ms2_score = major_ion_info.loc[row, "MS2 cosine score"]

                if(adduct == s["major_ion"]):
                    adduct_matches.append("Yes")

                else:
                    adduct_matches.append(f"No {adduct}")

                if (molecular_formula == s["molecular_formula"]):
                    molecular_formula_matches.append("Yes")

                else:
                    molecular_formula_matches.append(f"No {molecular_formula}")
                    if (ms1_match is np.nan):

                        ms1_matches.append("No match")

                    elif (s["name"].upper() in ms1_match.upper() ):
                        (ms1_matches.append(f"Yes (ppm = {ms1_ppm})"))

                    else:
                        ms1_matches.append(f"No {ms1_match} ppm = {ms1_ppm}")

                    if(ms2_match is np.nan):

                        ms2_matches.append("No match")

                    elif(s["name"].upper() in ms2_match.upper()):
                        (ms2_matches.append(f"Yes Score = {ms2_score}"))

                    else:
                        ms2_matches.append(f"No {ms2_match}")


    fg_info = pd.DataFrame({"Standard":fg_names,
                  "Feature_Group":fg_list})

    fg_info.to_csv("Feature_groups.csv")

    #information has been checked for all standards - change format and add index values for table concatenation
    adduct_matches = pd.Series(adduct_matches).set_axis(major_ion_matches.index.values)
    molecular_formula_matches = pd.Series(molecular_formula_matches).set_axis(major_ion_matches.index.values)
    ms1_matches = pd.Series(ms1_matches).set_axis(major_ion_matches.index.values)
    ms2_matches = pd.Series(ms2_matches).set_axis(major_ion_matches.index.values)
    compounds = pd.Series(compounds).set_axis(major_ion_matches.index.values)

    major_ion_matches = pd.concat([
        major_ion_matches,
        pd.Series(adduct_matches, name="Adduct Correct"),
        pd.Series(molecular_formula_matches, name="MF Correct"),
        pd.Series(ms1_matches, name="MS1 matches"),
        pd.Series(ms2_matches, name="MS2 matches")
        ],
        axis=1)


    #insert standard names in the first column position
    major_ion_matches.insert(loc=0,
                             column= "Standard",
                             value=compounds)

    print(os.path)
    major_ion_matches.to_csv("Correct_Annotation_Checks.csv")

    #plot standards feature quality
    plot_standards_fwhm(major_ion_matches, show_plot=True)
    plot_standards_asymmetry(major_ion_matches, show_plot=True)
    plot_standards_tailing(major_ion_matches, show_plot=True)
    plot_standards_isotopes(major_ion_matches, show_plot=True)
    plot_standards_charge(major_ion_matches, show_plot=True)
    plot_standards_frag_scans(major_ion_matches, show_plot=True)
    plot_standards_ms2_apex_dist(major_ion_matches, show_plot=True)
    plot_standards_area(major_ion_matches, show_plot=True)
    plot_standards_height(major_ion_matches, show_plot=True)

    #Check the size of feature groups and percentage of adducts within that are related to the standard
    feature_group_checker(full_peak_table, fg_info, 5)

    #Now matched have been found in te overall peak table check for the LORCD in the dilution series outputs
    dilution_order = [8, 5, 3, 9, 6, 4, 10, 7, 2, 1, 0]
    dilution_series_files = [dilution_series_files[i] for i in dilution_order]

    # dilution = 'Set1mix_LM4_400ug-mL_Peak_Table.xlsx'
    # id = dilution_df.index.values[0]

    dilution_series_df = pd.DataFrame().set_axis(major_ion_matches.index.values)

    #check each dilution series output
    for dilution in dilution_series_files:

        dilution_df = pd.read_excel(dilution,
                                    index_col=0)

        avg_height_list = []

        #check for presence of each peak of interest found in the full peak table by shared peak id values (indices)
        for id in major_ion_matches.index.values:

            #is the peak id of interest found in the filtered dilution outputs?
            if id in dilution_df.index.values:

                avg_height = dilution_df.loc[id,"Avg Height"]
                avg_height_list.append(avg_height)

            else:

                avg_height_list.append(0)


        avg_height_list = pd.Series(avg_height_list).set_axis(major_ion_matches.index.values)
        dilution_series_df = pd.concat([dilution_series_df, avg_height_list], axis=1)

    conc_labels = ["400 ug/mL",
                   "200 ug/mL",
                   "100 ug/mL",
                   "50 ug/mL",
                   "25 ug/mL",
                   "12.5 ug/mL",
                   "6.25 ug/mL",
                   "3.125 ug/mL",
                   "1.5625 ug/mL",
                   "0.78125 ug/mL",
                   "0.390625 ug/mL",]

    dilution_series_df.columns = conc_labels
    dilution_series_df.insert(loc=0,
                             column= "Standard",
                             value=compounds)

    dilution_series_df.to_csv("LORCD_filtered_outputs.csv")

    #full_peak_table = ([s for s in files if "Final" in s])
    #peak_table_heights = pd.read_excel(full_peak_table[0],index_col=0, sheet_name="All_Stats",encoding="utf-8-sig")
    peak_table_heights = bio_stats
    peak_table_heights.index = peak_table_heights.index.astype(int)

    dilution_series_cols = dilution_series_files
    dilution_series_cols = [d[:-16] for d in dilution_series_cols]
    dilution_series_cols = [d + "_avg" for d in dilution_series_cols]

    dilution_series_df2 = pd.DataFrame().set_axis(major_ion_matches.index.values)

    # print(dilution_series_cols)
    # print(peak_table_heights.columns)

    #check each dilution series output
    for dilution in dilution_series_cols:

        #print(f"current dilution is {dilution}")

        avg_height_list = []

        #check for presence of each peak of interest found in the full peak table by shared peak id values (indices)
        for row_ids in major_ion_matches.index.values:

                #print(f"current feature id is {row_ids}")

                #try:
                avg_height = peak_table_heights.loc[row_ids, dilution]
                # except KeyError:
                #     avg_height = ("KeyError")
                #     continue

                avg_height_list.append(avg_height)

        avg_height_list = pd.Series(avg_height_list).set_axis(major_ion_matches.index.values)
        dilution_series_df2 = pd.concat([dilution_series_df2, avg_height_list], axis=1)

    dilution_series_df2.columns = conc_labels
    dilution_series_df2.insert(loc=0,
                               column="Standard",
                               value=compounds)
    dilution_series_df2.to_csv("LORCD.csv")

    dilution_series_df2 = dilution_series_df2.drop("Standard", axis=1)

    return fg_info



















