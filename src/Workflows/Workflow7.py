#This workflow includes all four main sample types
# Bio, Media/Control, Blanks, QCs
# Blank Subtraction implemented
# Multi Bio Single control FCs
# QC data present - PCA plotted

from src.assign_global_variables import path, peaklist, Blank_identifier, QC_identifier
from src.Avg_height_hists import plot_peak_height_hist
from src.Avg_SD_RSD_calcs import avg_sd_rsd
from src.Blank_Filtering import blank_filter
from src.detect_sample_groups import detect_sample_groups
from src.Export_Peak_Table import export_PT
from src.FC_calculator import FC_MultiBio_vs_SingleControl
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Fraction_filter import fraction_filter
from src.get_group_heights import get_single_group_heights
from src.ID_levels import ID_levels
from src.MVI import random_forest_MVI
from src.MZMine3_columns import mzmine3_cols
from src.MZMine3_module_divider import divide_mzmine3_table
from src.Normalisation import sum_normalisation_raw
from src.PCA import plot_PCA
from src.Plot_RSDs import plot_rsd_vs_rt
from src.QC_Filter import QC_Filter
from src.read_peak_table import read_mzmine3_peaktable
from src.sample_names import get_sample_names
from src.Transformation import transformation_single

#Read in and organise the peak table and detect sample groups
mzmine3 = read_mzmine3_peaktable(path, peaklist)
cols = mzmine3_cols(mzmine3)
mods = divide_mzmine3_table(mzmine3, cols)
names = get_sample_names(mods[6])
groups = detect_sample_groups(names)
heights = get_single_group_heights(mods[6], names)

#Calculate summary stats for all features in all groups
bio_stats = avg_sd_rsd(heights[0], groups[4], groups[0])
media_stats = avg_sd_rsd(heights[1], groups[5], groups[1])
blank_stats = avg_sd_rsd(heights[2], Blank_identifier, groups[2])
qc_stats = avg_sd_rsd(heights[3], QC_identifier, groups[3])

#Blank Filtering
blank_i_filt = blank_filter(bio_stats, media_stats, qc_stats, blank_stats)
bio_stats = single_table_filt(blank_i_filt, bio_stats)
media_stats = single_table_filt(blank_i_filt, media_stats)
qc_stats = single_table_filt(blank_i_filt, qc_stats)
mods_blank_filt = module_tables_filt(blank_i_filt, mods)

#plot feature reproducibility across the run
plot_rsd_vs_rt(bio_stats, media_stats, qc_stats, mods_blank_filt[7], show_plot=True)

#Calculate FCs
FC_table = FC_MultiBio_vs_SingleControl(groups[4], bio_stats, media_stats)

#Add levels of ID
ID_levels(mods_blank_filt)

#Export peak table for the whole dataset
export_PT(mods_blank_filt, FC_table, bio_stats, media_stats, qc_stats, blank_stats, heights)

#Export stringently filtered peak tables for individual biological samples
fraction_filter(bio_stats, groups[4], FC_table, mods_blank_filt)

#PCA production
#filter on qc RSDs
QC_filt = QC_Filter(qc_stats, 30)
bio_stats = single_table_filt(QC_filt, bio_stats)
media_stats = single_table_filt(QC_filt, media_stats)
qc_stats = single_table_filt(QC_filt, qc_stats)
mods_qc_filt = module_tables_filt(QC_filt, mods)

#plot heights of QC filtered peaks
plot_peak_height_hist(mods_qc_filt[6], "QC_filt_peak_heights", show_fig="True")

#perform sum normalisation on raw QC filtered peaks intensities
norm_heights = sum_normalisation_raw(mods_qc_filt[6])
#plot heights of sum normalised QC filtered peaks
plot_peak_height_hist(norm_heights, "QC_filt_normalised_peak_heights", show_fig="True")

#impute missing values with random forest imputation
RFI_heights = random_forest_MVI(norm_heights, 5, 100)

#plot heights of RF imputed, sum normalised QC filtered peaks
plot_peak_height_hist(RFI_heights, "QC_filt_RF_imputed_normalised_peak_heights", show_fig="True")

#transform
trans_heights = transformation_single(RFI_heights, "log2")
#plot heights of RF imputed, sum normalised, log2 transformed QC filtered peaks
plot_peak_height_hist(trans_heights, "QC_filt_log2_tranformed_RF_imputed_normalised_peak_heights", show_fig="True")

#PCA
plot_PCA(trans_heights, groups[4], groups[5])







