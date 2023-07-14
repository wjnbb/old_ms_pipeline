# Bio, Media/Control, Blanks, QCs
# Blank Subtraction implemented
# Single Bio Single control FCs

from src.assign_global_variables import path, peaklist, Blank_identifier, QC_identifier
from src.Avg_SD_RSD_calcs import avg_sd_rsd
from src.Blank_Filtering import blank_filter
from src.detect_sample_groups import detect_sample_groups
from src.Export_Peak_Table import export_PT
from src.FC_calculator import FC_SingleBio_vs_SingleControl
from src.Filter_Row_Indices import single_table_filt, module_tables_filt
from src.Fraction_filter import fraction_filter
from src.get_group_heights import get_group_heights
from src.ID_levels import ID_levels
from src.MZMine3_columns import mzmine3_cols
from src.MZMine3_module_divider import divide_mzmine3_table
from src.Plot_RSDs import plot_rsd_vs_rt
from src.read_peak_table import read_mzmine3_peaktable
from src.sample_names import get_sample_names

#Read in and organise the peak table and detect sample groups
mzmine3 = read_mzmine3_peaktable(path, peaklist)
cols = mzmine3_cols(mzmine3)
mods = divide_mzmine3_table(mzmine3, cols)
names = get_sample_names(mods[6])
groups = detect_sample_groups(names)
heights = get_group_heights(mods[6], groups[4], groups[5], groups[2], groups[3])

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
plot_rsd_vs_rt(bio_stats, media_stats, qc_stats, mods_blank_filt[7], show_plot=False)

#Calculate FCs
FC_table = FC_SingleBio_vs_SingleControl(bio_stats, media_stats, BG_ignore="Load")

#Add levels of ID
ID_levels(mods_blank_filt)

#Export peak table for the whole dataset
export_PT(mods_blank_filt, FC_table, bio_stats, media_stats, qc_stats, blank_stats, heights)









