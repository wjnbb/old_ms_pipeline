import os
import pandas as pd
import numpy as np
import plotly.express as px

#round1 data
#path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230806_MS2_optimisation_R1"

#datasets = ["M1_AH02", "M2_AH02", "M3_AH02", "M4_AH02", "M5_AH02", "M6_AH02", "M7_AH02", "M8_AH02", "M9_AH02", "M10_AH02",
#            "M11_AH02", "M12_AH02", "M13_AH02", "M14_AH02", "M15_AH02", "M16_AH02", "M17_AH02", "M18_AH02", ]

#path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230808_MS2_optimisation_R3/"

#datasets = ["M3_AF05", "M3_v2_AF05", "M6_AF05", "M6_v2_AF05", "M9_AF05", "M9_v2_AF05"]
#datasets = ["M3_SST", "M3_v2_SST", "M6_SST", "M6_v2_SST", "M9_SST", "M9_v2_SST"]

#path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230810_HetEx_Pp_AF05"
#datasets = ["20230810_HetEx_Pp_AF05_V1", "20230810_HetEx_Pp_AF05_V2", "20230810_HetEx_Pp_AF05_V3", "20230810_HetEx_Pp_AF05_V4"]

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230816_SST_collision_energies"
datasets = ["AA15_SSTsp_CE30", "AA15_SSTsp_formula1", "AA15_SSTsp_formula2", "AA23_SSTsp_CE30", "AA23_SSTsp_formula1",
            "AA23_SSTsp_formula2", "AA43_SSTsp_CE30", "AA43_SSTsp_formula1", "AA43_SSTsp_formula2"]

os.chdir(path)

summary_table = pd.DataFrame()

#d = "20230810_HetEx_Pp_AF05_V1"

for d in datasets:

    os.chdir(path)

    os.chdir(d)

    # read in the peak table from the working directory
    peak_table = pd.read_csv("MZMine3/peaklist.csv", index_col=0)

    #get total number of features
    feature_num = len(peak_table)

    #get peak heights to calculate rsds, replace NAs with 10
    heights = peak_table[[s for s in peak_table.columns if "height" in s][1:]].fillna(1000)
    #heights = heights[[s for s in heights.columns if "AF05" in s]]

    #get the average height for each feature
    height_avg = heights.mean(axis=1)

    #get the standard deviation for each featrue
    height_std = heights.std(axis=1)

    #get the relative standard deviation for each feature
    height_rsd = (height_std/height_avg)*100

    #get the number of features with RSD less than 30
    height_RSD_30_num = np.count_nonzero(height_rsd <= 30.0)

    #get the percentage of features with less than 30% RSD
    height_RSD_30_perc = (height_RSD_30_num/feature_num)*100

    # get peak heights to calculate rsds, replace NAs with 10
    areas = peak_table[[s for s in peak_table.columns if "area" in s][1:]].fillna(1000)
    #areas = areas[[s for s in areas.columns if "AF05" in s]]

    #get the average height for each feature
    area_avg =areas.mean(axis=1)

    #get the standard deviation for each featrue
    area_std = areas.std(axis=1)

    #get the relative standard deviation for each feature
    area_rsd = (area_std/area_avg)*100

    #get the number of features with RSD less than 30
    area_RSD_30_num = np.count_nonzero(area_rsd <= 30.0)

    #get the percentage of features with less than 30% RSD
    area_RSD_30_perc = (area_RSD_30_num/feature_num)*100

    #get the number of features with MS2 collected
    ms2_collected = np.count_nonzero(peak_table["fragment_scans"])

    #get the percentage of features with MS2 collected
    ms2_perc = (ms2_collected/feature_num)*100

    #get the number of features with an MS2 match
    ms2_matches = np.count_nonzero(peak_table["spectral_db_matches:cosine_score"] >= 0.5)

    #good quality MS2 match
    good_ms2_match = np.count_nonzero(peak_table["spectral_db_matches:cosine_score"] >= 0.7)

    #high quality MS2 match
    high_ms2_match = np.count_nonzero(peak_table["spectral_db_matches:cosine_score"] >= 0.9)

    #get the number of features with an MS2 match
    ms2_matches_signal_num = np.count_nonzero((peak_table["spectral_db_matches:cosine_score"] >= 0.5) & (peak_table["spectral_db_matches:n_matching_signals"] >= 4))

    #good quality MS2 match
    good_ms2_match_signal_num = np.count_nonzero((peak_table["spectral_db_matches:cosine_score"] >= 0.7) & (peak_table["spectral_db_matches:n_matching_signals"] >= 4))

    #high quality MS2 match
    high_ms2_match_signal_num = np.count_nonzero((peak_table["spectral_db_matches:cosine_score"] >= 0.9) & (peak_table["spectral_db_matches:n_matching_signals"] >= 4))

    one_signal_matches_percentage = ((np.count_nonzero(peak_table["spectral_db_matches:n_matching_signals"] == 3))/ms2_matches)*100

    fig = px.violin(peak_table, y="spectral_db_matches:cosine_score")

    fig.write_html("MS2_match_score_violin_plot.html")

    M_results = [feature_num,
                 height_RSD_30_num,
                 height_RSD_30_perc,
                 area_RSD_30_num,
                 area_RSD_30_perc,
                 ms2_collected,
                 ms2_perc,
                 ms2_matches,
                 good_ms2_match,
                 high_ms2_match,
                 ms2_matches_signal_num,
                 good_ms2_match_signal_num,
                 high_ms2_match_signal_num,
                 one_signal_matches_percentage]

    D_results = pd.DataFrame([height_avg,
                 height_std,
                 height_rsd,
                 area_avg,
                 area_std,
                 area_rsd,
                 peak_table["spectral_db_matches:cosine_score"],
                 peak_table["fragment_scans"]])

    # # # Make an RSD vs RT plot for each group
    # fig = px.scatter(D_results, x="rt", y=c)
    #
    #      if show_plot == True:
    #          fig.show()
    #
    # fig.write_html(path + "RSD_plots/" + d + ".html")


    summary_table = pd.concat([summary_table, pd.Series(M_results)], axis=1)


#rename the columns
summary_table.columns = datasets

#transpose
summary_table = summary_table.T

summary_table.columns = ["Total_features", "Height_RSD_30", "Height_RSD_30_perc", "Area_RSD_30",
                         "Area_RSD_30_perc", "MS2_collected", "MS2_feature_perc", "MS2_matches",
                         "MS2_matches_70", "MS2_matches_90", "MS2_matches_signal_num",
                         "MS2_matches_70_signal_num", "MS2_matches_90_signal_num", "2_signal_match_perc"]

os.chdir("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Agilent_Method_Development/MS_results")

summary_table.to_csv('MS2_opt_results_summary.csv', index = True)

# read in the peak table from the working directory
#peak_table = pd.read_csv("MS2_opt_results_summary.csv")

import plotly.express as px