import pandas as pd
import os
import numpy as np
from src.ppm_calculator import ppm_calculator
import plotly.express as px

def feature_group_checker(full_peak_table, fg_info, ppm):

    print(f"Printing working directory in feature group checker {os.getcwd()}")

    #import the precalculated adduct masses for each standard
    standards_adducts = pd.read_csv("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/Standards_adducts_set1and2.csv",
                          index_col=0)
    standards = list(np.unique(fg_info["Standard"]))
    #full_peak_table = pd.read_excel(full_peak_table[0], index_col=0)

    #seed lists for storing total results for all standards and groups
    matched_fg = []
    matched_mzs = []
    matched_adducts = []
    fg_sizes = []
    matched_standards = []

    #loop through the standards in the output
    for standard in standards:

        #print(f"investigating {standard}")
        #get the feature group numbers for the current standard
        feature_groups = fg_info.loc[(fg_info["Standard"] == standard), "Feature_Group"]
        #get the precalculated masses for the different adducts for the current standard
        adduct_masses = (standards_adducts.loc[:, standard])[1:]

        #loop through the different feature groups this standard was found in
        for fg in feature_groups:

            #print(f"Feature group {fg} being investigated")
            #assign all mz values in the current feature group to a variable to loop through
            fg_mzs = full_peak_table.loc[(full_peak_table["feature_group"] == fg),"mz"]
            #get size of the feature group and append to fg_sizes list
            #print(f"{len(fg_mzs)} features are present in the feature group")

            #loop through the mzs in the feature group
            for mz in fg_mzs:

                #print(f"Checking first experimental mz ({mz})")

                #loop through the adduct masses to check against
                for ad_mass in adduct_masses:

                    #calculate a min and max value for the adduct mass
                    #print(f"Checking adduct masses for matches")
                    ad_mass_error = ppm_calculator(ad_mass, ppm)
                    ad_mass_max = ad_mass+ad_mass_error
                    ad_mass_min = ad_mass-ad_mass_error

                    #check if the experimental mz is within the ppm error bounds calculated above
                    if((mz <= ad_mass_max) & (mz >= ad_mass_min)):

                        #if a match is found then add the relevant info to the result variables
                        #print(f"Adduct matched!!! Matched mz is {mz} and this corresponds to {adduct_masses[adduct_masses == ad_mass].index[0]}")
                        matched_fg.append(fg)
                        matched_mzs.append(mz)
                        matched_adducts.append(adduct_masses[adduct_masses == ad_mass].index[0])
                        matched_standards.append(standard)
                        fg_sizes.append(len(fg_mzs))

    #concatenate the 5 result lists
    fg_stats = pd.concat([pd.Series(matched_standards),
                               pd.Series(matched_fg),
                               pd.Series(matched_mzs),
                               pd.Series(matched_adducts),
                               pd.Series(fg_sizes)], axis=1)

    #add column names
    fg_stats.columns = ["Standards", "Feature_Group", "Experimental_m/z", "Matched_Adduct", "Feature_Group_Size"]

    #seed variabe for storing percentage adduct matching results
    fg_match_percentages = []

    #loop through the rows the feature group stats generated to calculate the percentage adduct matching for each group
    for r in fg_stats.index:

        #get the fg number, standard name and total fg size for this row
        fg = fg_stats.iloc[r,1]
        standard = fg_stats.iloc[r, 0]
        fg_total_num = fg_stats.iloc[r, 4]

        #count the number of rows(matched adducts) for this feature group/standard combo
        match_num = len(fg_stats[(fg_stats["Feature_Group"] == fg) & (fg_stats["Standards"] == standard)])

        #calculate the percentage of the group that can be related to the standard
        fg_match_percentage = (match_num/fg_total_num)*100
        fg_match_percentages.append(fg_match_percentage)


    fg_stats = pd.concat([fg_stats,
                                     pd.Series(fg_match_percentages)],
                                     axis=1)

    fg_stats.columns.values[5]= "FG_match_percentages"

    fg_stats.to_csv("Feature_Group_Stats.csv")

    fig = px.scatter(fg_stats,
                     x=fg_stats["FG_match_percentages"],
                     y=fg_stats["Feature_Group_Size"],
                     color=fg_stats["Standards"]
                     )

    fig.update_layout(
        xaxis_title="% of Features in Feature Group Confirmed as Related to the Standard",
        yaxis_title="# of Features in the Feature Group",
        legend_title="Standards"
    )

    fig.write_html("FG Match % vs FG Size.html")

    #print(fg_stats["Matched_Adduct"].value_counts())
    adduct_counts = fg_stats["Matched_Adduct"].value_counts()

    #test_df.rename("Count")
    adduct_counts_df = pd.DataFrame(adduct_counts)

    adduct_counts_df.columns.values[0] = "Count"

    fig = px.bar(adduct_counts_df,
                 x=adduct_counts_df.index.values,
                 y=adduct_counts_df["Count"]
                 )

    fig.update_layout(
        xaxis_title="Ion Annotation",
        yaxis_title="Count"
    )

    fig.write_html("Adduct Frequency.html")

    return adduct_counts_df










