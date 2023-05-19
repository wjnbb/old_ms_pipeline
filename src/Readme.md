# MZMine3 Peak Table Manipulation and Analysis

 A series of functions/workflows to manipulate the MZMine3 peak tables for the end user/s.

## Functions

### read_mzmine3_peaktable(path, raw_peak_table)

Takes a string filepath (path) and string filename (raw_peak_table) of a csv MZMine3 peak table this and returns it as 
a Pandas dataframe after setting the row indices to the row/feature ID numbers exported by MZMine3.

### mzmine3_cols(peak_table)

Takes a MZMine3 peak table as a Pandas dataframe and extracts all the column names as a list.

### divide_mzmine3_table(peak_table, p_cols)

Takes a list of MZMine3 column names and uses the consistent prefixes for the different processing modules to divide
it into a separate dataframe for each processing module applied as well as a peak height matrix.

8 Pandas dataframes should be generated for the prefixes below and the dataframes are returned as part of a tuple and
stored in the following order.

1. compound_db_identity - Corresponds to MS1 database matching results
2. spectral_db_matches - Corresponds to MS2 spectral matching results
3. formulas - Corresponds to molecular formula prediction results
4. alignment_scores - Corresponds to the feature alignment quality scores
5. ion_identities - Corresponds to the ion identity networking results
6. manual_annotation - Corresponds to the manual annotation notes
7. datafile - Corresponds to the peak height data for all samples
8. no prefix - Corresponds to the average data for the feature row (mz, rt, charge etc)

### get_sample_names(height_df)

Takes a pandas dataframe of MZMine3 peak height data and then extracts all the sample names in the batch from within the
column headers. Returns a list of all the sample names.

### detect_sample_groups(sample_names)

Takes a list of sample names and detects and divides samples into biological, blank, media/control and QC sample groups 
based on the strings provided for Bio_identifier, Blank_identifier, Media_identifier, QC_identifier, and their presence
in the sample names. Biological and Media/Control samples may be divided into further subgroups.

Returns a tuple of 6 lists containing the sample groups in the following order.

1. Biological samples
2. Media/Control samples
3. Blank samples
4. QC samples
5. Biological sample subgroups
6. Media/Control sample subgroups

### get_group_heights(height_df, Bio, Media, Blanks, QCs)

Takes a MZMine3 peak height Pandas dataframe and lists of the samples contained within the biological, media/control,
blank and QC sample groups. Returns a tuple of four Pandas dataframes dividing the peak height data into their separate
groups in the following order..

1. Biological samples
2. Media/Control samples
3. Blank samples
4. QC samples

### avg_sd_rsd(df, groups, grp_names)

Takes the peak height Pandas dataframe for a sample group (Biolgical, Media/Control, Blank or QC), the group identifier
(for blanks and QCs) or list of subgroups (for biological or media/controls) as well as the list of all samples names
in the group. The peak height average, standard deviation and relative standard deviation are calculated for each feature
in each group/subgroup. Returns a Pandas dataframe containing all calculated statistics for the group.

### blank_filter(Bio_stats, Media_stats, QC_stats, Blank_stats)

Takes the peak height stats (avg, sd, rsd) calculated for each sample group and identifies all feature rows for which no
biological, media or QC sample average height in the dataset exceeded a minimum FC as specified by the Blank_thresh
variable versus the average height of the blank samples and returns a list of the indices of those rows.

### QC_Filter(QC_stats, QC_RSD_thresh)

Takes a Pandas dataframe of QC sample peak height stats and a percentage RSD threshold and returns a list of feature/rows
indices which don't meet the QC sample RSD threshold.

### module_tables_filt(filt_indices, module_tables)

Takes a list of row indices and a tuple of Pandas dataframes and filters by row using the indices for each dataframe
within the tuple. Returns a tuple of row filtered Pandas dataframes.

### single_table_filt(filt_indices, df)

Takes a list of row indices to filter out the relevant rows and a Pandas dataframe of the peak height stats for the
group in question. Returns a filtered pandas dataframe of peak height stats.

### plot_rsd_vs_rt(Bio_stats, Media_stats, QC_stats, peak_info)

Creates a simple scatter plot for each sample group in the dataset of the feature RSD vs RT to assess feature 
reproducibility across the LC-MS run. A new directory is made within the working directory to save the plots into.

### FC_SingleBio_vs_SingleControl(Bio_stats, Media_stats)

Takes a Pandas dataframe of the biological sample group peak height stats and another of the media/control group peak
height stats. Returns a Pandas dataframe of the FC of the average biological sample peak height vs the average
media/control sample peak height.

### FC_MultiBio_vs_SingleControl(Bio_groups, Bio_stats, Control_stats)

Takes a list of multiple biological sample groups, the average peak height stats for biological sample groups and 
media/control sample group as separate Pandas dataframes. Returns a Pandas dataframe of the fold changes for the
multiple biological groups average peak height vs the single control/media group average peak height.

### FC_MultiBio_vs_MultiControl(Bio_groups, Bio_stats, Media_stats)

Takes a list of multiple biological sample groups, the average peak height stats for biological sample groups and 
media/control sample group as separate Pandas dataframes. The supplied bio_media_linkers list ensures linking of the
correct biological group to the relevant media/control group. Returns a Pandas dataframe of the fold changes for the
multiple biological groups average peak height vs the partner control/media group average peak height.

### QC_normalisation(QC_stats, Bio_stats, Media_stats)

Takes Pandas dataframes of peak height stats for QC, biological and media/control sample groups. Biological and
media/control feature height averages are divided by the QC average height for that feature to generate a QC
normalised peak height. Returns a tuple of pandas dataframes containing the QC normalised peak height data.

### export_PT(module_tables, FC_Stats, Bio_stats, Media_stats, QC_stats, Blank_stats, group_heights)

Takes the list of MZMine3 processing module Pandas dataframes, fold change stats dataframe, biological, media/control,
QC and blank peak height stats dataframes and raw peak height data and exports it to a .xlsx file. Data is separated out
into different sheets with key data from some of the MZMine3 processing modules collated into the first sheet. Each
processing module from MZMine has the complete data in its own tab. The file is saved into the current working directory.

### export_PT_w_norm(module_tables, FC_Stats, Bio_stats, Media_stats, QC_stats, Blank_stats, group_heights, norm_heights)

Takes the list of MZMine3 processing module Pandas dataframes, fold change stats dataframe, biological, media/control,
QC and blank peak height stats dataframes, raw peak height data and normalised peak height data and exports it to a
.xlsx file. Data is separated out into different sheets with key data from some of the MZMine3 processing modules
collated into the first sheet. Each processing module from MZMine has the complete data in its own tab. The file is
saved into the current working directory.

### export_PT_noFC(module_tables, Bio_stats, Media_stats, QC_stats, Blank_stats, group_heights)

Takes the list of MZMine3 processing module Pandas dataframes, biological, media/control, QC and blank peak height stats
dataframes, raw peak height data and normalised peak height data and exports it to a .xlsx file. Data is separated out
into different sheets with key data from some of the MZMine3 processing modules collated into the first sheet. Each
processing module from MZMine has the complete data in its own tab. The file is saved into the current working directory.





