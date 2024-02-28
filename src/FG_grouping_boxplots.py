import os
import pandas as pd
import plotly.express as px
import numpy as np
#get the list of datasets to analyse
path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/FG_investigation_results/"
os.chdir(path)
datasets = os.listdir(path)[2:]

#dataset = datasets[0]

all_datasets_standards_data = pd.DataFrame()
all_datasets_summary_data = pd.DataFrame()

for dataset in datasets:

    #read in the summary data for the whole dataset
    fg_data_dataset = pd.read_csv(f"{path}{dataset}/FG_summary_dataset.csv", index_col=0)
    fg_data_dataset.columns.values[0] = dataset.removeprefix("output_")
    all_datasets_summary_data = pd.concat([all_datasets_summary_data, fg_data_dataset], axis=1)

    #read in the data for the standards fg info
    fg_data_standards = pd.read_csv(f"{path}{dataset}/FG_summary_standards.csv")
    fg_data_standards = fg_data_standards[fg_data_standards.Standard1 != "Fosfomycin"]
    fg_data_standards = fg_data_standards.reset_index(drop=True)

    #create series of the parameter values equal to the number of rows of standards data there are for each dataset
    rt_tol = pd.Series(np.repeat(((dataset.removeprefix("output_")).split("_")[0]), 15),
                       name = "RT Tolerance (mins)")
    shape_corr = pd.Series(np.repeat(((dataset.removeprefix("output_")).split("_")[1]), 15),
                           name = "Feature Shape Correlation")
    height_corr = pd.Series(np.repeat(((dataset.removeprefix("output_")).split("_")[2]), 15),
                            name = "Feature Height Correlation")
    dataset_label = pd.Series(np.repeat(dataset.removeprefix("output_"), 15),
                              name="Dataset Label")

    #combine the standards data info for all metrics into a df structure ready for plotting
    avg_FG_size = fg_data_standards["Average FG Size"]
    avg_FG_accuracy = fg_data_standards["Average FG Accuracy"]
    fg_filt_lorcd = fg_data_standards["FG_Filt_LORCD ug/mL"]
    avg_unique_fg = fg_data_standards["Unique FG Count"]
    fg_filt_diff = pd.Series((pd.to_numeric((fg_data_standards["FG_Filt_LORCD ug/mL"])))-(pd.to_numeric((fg_data_standards["LORCD ug/mL"]))),
                             name="FG Filter LORCD differential")
    standards = fg_data_standards["Standard1"]
    fg_dataset_standards = pd.concat([
                                    standards,
                                    dataset_label,
                                    rt_tol,
                                    shape_corr,
                                    height_corr,
                                    avg_FG_size,
                                    avg_FG_accuracy,
                                    fg_filt_lorcd,
                                    fg_filt_diff,
                                    avg_unique_fg
                                    ],
                                    axis=1
                                )
    all_datasets_standards_data = pd.concat([
                                    all_datasets_standards_data,
                                    fg_dataset_standards
                                    ],
                                    axis=0
                               )

all_datasets_summary_data = all_datasets_summary_data.transpose()

fig = px.bar(all_datasets_summary_data,
             x=all_datasets_summary_data.index.values,
             y="Multi-standard FG Counts",
             title="Multi-standard FG Counts")

fig.update_layout(xaxis_title="Dataset",
                  yaxis_title="Multi-standard FG Counts")

fig.write_html(f"{path}graph_outputs/Multi-standard_FG_count_barplot.html")


    # avg_FG_size_df = pd.melt(avg_FG_size_df)
    # avg_FG_size_df.columns.values[0:1] = ["Dataset", "Average FG Size per Standard"]
    # avg_FG_size_df.columns = ["Dataset", "Average FG Size per Standard"]

#convert RT tolerance column to numeric
all_datasets_standards_data["RT Tolerance (mins)"] = pd.to_numeric(all_datasets_standards_data["RT Tolerance (mins)"])

fig = px.box(all_datasets_standards_data,
             x="RT Tolerance (mins)",
             y="Unique FG Count",
             color="Feature Height Correlation",
             title="Unique FG Count Per Standard with different Feature Grouping Parameters"
             )

fig.update_layout(xaxis_title="Dataset",
                  yaxis_title="Unique FG Count per Standard")

fig.write_html(f"{path}graph_outputs/Unique FG Count_boxplot_by_feature_height_correlation.html")



fig = px.scatter(all_datasets_standards_data,
             x="Average FG Size",
             y="Average FG Accuracy",
             color="Dataset Label",
             symbol="Standard1",
             title="Average FG Size vs Average FG Accuracy with different Feature Grouping Parameters"
             )

fig.update_layout(xaxis_title="Average FG Size",
                  yaxis_title="Average FG Accuracy (%)")

fig.write_html(f"{path}graph_outputs/FG_accuracy_vs_FG_size.html")
os.mkdir("graph_outputs/FG_Size_vs_Accuracy_per_standard")

for standard in standards:

    all_datasets_standards_data_s = all_datasets_standards_data[all_datasets_standards_data["Standard1"] == standard]

    fig = px.scatter(
                    all_datasets_standards_data_s,
                    x="Average FG Size",
                    y="Average FG Accuracy",
                    color="Feature Shape Correlation",
                    symbol="Feature Height Correlation",
                    size="RT Tolerance (mins)",
                    title=f"{standard} Feature Group Size vs Feature Group Accuracy "
                 )

    fig.update_layout(xaxis_title="Average Feature Group Size",
                      yaxis_title="Average FG Accuracy (%)")

    fig.write_html(f"{path}graph_outputs/FG_Size_vs_Accuracy_per_standard/FG_size_vs_accuracy_scatter_by_{standard}"
                   f"_2.html")






