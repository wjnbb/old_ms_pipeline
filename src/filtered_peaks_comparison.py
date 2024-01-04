import pandas as pd
import os

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230822_HetEx007_AHLc/MZMine3"

os.chdir(path)

full_peak_table = pd.read_excel("Final_Peak_Table_20230822_HetEx007_AHLc.xlsx", index_col=0)

df1 = pd.read_excel("AB03_AHLc_LM2_Peak_Table.xlsx", index_col=0)
df2 = pd.read_excel("AB03_norm_LM2_Peak_Table.xlsx", index_col=0)
df3 = pd.read_excel("Pp_AB03_3.5FC_AHLc_Peak_Table.xlsx", index_col=0)
df4 = pd.read_excel("Pp_AB03_3.5FC_NoI_Peak_Table.xlsx", index_col=0)

df1_i = df1.index

AB03_WT_peaks = set(df1.index) & set(df2.index)
hetex_peaks = set(df3.index) & set(df4.index)

ab = set(hetex_peaks) & set(AB03_WT_peaks)

hetex_filt = df3.filter(items=hetex_peaks, axis=0)
wt_filt = df1.filter(items=AB03_WT_peaks, axis=0)

ab_filt = df1.filter(items=ab, axis=0)

ab_filt.to_csv(ab_filt, encoding='utf-8', index=False)

ab_filt.to_csv("antibiotic.csv", index = True, header=True)
hetex_filt.to_csv("HetEx_peaks.csv", index=True, header=True)
wt_filt.to_csv("AB03_WT_peaks.csv", index=True, header=True)