#code to add identification information to allow processing of MZMIne outputs without MS1, MS2 and MF prediction info

import os
import pandas as pd
import numpy as np

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/FG_investigation_results/"

os.chdir(path)

datasets = os.listdir(path)[61:]

# dataset = datasets

for dataset in datasets:

    os.chdir(f"{path}{dataset}")

    peaklist = pd.read_csv(f"{dataset}.csv", index_col=0)

    # peaklist.insert(loc=46,
    #                 column="spectral_db_matches:cosine_score",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=47,
    #                 column="spectral_db_matches:precursor_mz",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=48,
    #                 column="compound_db_identity:mz_diff_ppm",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=49,
    #                 column="formulas:combined_score",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=50,
    #                 column="spectral_db_matches:compound_name",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=51,
    #                 column="compound_db_identity:compound_name",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=52,
    #                 column="formulas:formulas",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    # peaklist.insert(loc=53,
    #                 column="spectral_db_matches:spectral_db_matches",
    #                 value=pd.Series(0, index=np.arange(len(peaklist)+1)))

    peaklist["compound_db_identity:compound_name"] = peaklist["compound_db_identity:compound_name"].replace(0, "Module_not_run")
    peaklist["compound_db_identity:compound_name"] = peaklist["compound_db_identity:compound_name"].fillna("Module_not_run")

    # peaklist["spectral_db_matches:compound_name"] = peaklist["spectral_db_matches:compound_name"].replace(0, "Module_not_run")
    # peaklist["spectral_db_matches:compound_name"] = peaklist["spectral_db_matches:compound_name"].fillna("Module_not_run")
    #
    # peaklist["formulas:formulas"] = peaklist["formulas:formulas"].replace(0, "Module_not_run")
    # peaklist["formulas:formulas"] = peaklist["formulas:formulas"].fillna("Module_not_run")
    #
    # if "spectral_db_matches:spectral_db_matches" in peaklist.columns:
    #
    #     peaklist["spectral_db_matches:spectral_db_matches"] = peaklist["spectral_db_matches:spectral_db_matches"].replace(0, "Module_not_run")
    #     peaklist["spectral_db_matches:spectral_db_matches"] = peaklist["spectral_db_matches:spectral_db_matches"].fillna("Module_not_run")
    #
    # else:
    #     peaklist.insert(loc=53,
    #                     column="spectral_db_matches:spectral_db_matches",
    #                     value=pd.Series(0, index=np.arange(len(peaklist)+1)))
    #
    #     peaklist["spectral_db_matches:spectral_db_matches"] = peaklist[
    #         "spectral_db_matches:spectral_db_matches"].replace(0, "Module_not_run")
    #     peaklist["spectral_db_matches:spectral_db_matches"] = peaklist[
    #         "spectral_db_matches:spectral_db_matches"].fillna("Module_not_run")

    peaklist.to_csv(f"{dataset}.csv")


# "spectral_db_matches:compound_name"
# "compound_db_identity:compound_name"
# "formulas:formulas"
# "spectral_db_matches:cosine_score"
# "spectral_db_matches:precursor_mz"
# "compound_db_identity:mz_diff_ppm"
# "formulas:combined_score"



