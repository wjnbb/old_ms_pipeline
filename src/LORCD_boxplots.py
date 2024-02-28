import pandas as pd
import os
import plotly.express as px

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/"

lorcd_summary = pd.read_csv(f"{path}LORCD_summary.csv")
lorcd_summary = pd.melt(lorcd_summary, id_vars="Standard")

lorcd_summary.columns.values[2] = "LORCD"
lorcd_summary.columns.values[1] = "Background Matrix"

fig = px.box(lorcd_summary,
             x="Background Matrix",
             y="LORCD",
             color="Background Matrix",
             title="LORCD per background matrix across all standards",
             points="all")

fig.update_layout(xaxis_title = "Background Matrix",
                  yaxis_title = "LORCD (Limit of reproducible computational detection) (μg/mL)")

fig.write_html(f"{path}LORCD_boxplots_per_background.html")



# lorcd_summary = pd.read_csv(f"{path}LORCD_summary.csv")
# lorcd_summary = pd.melt(lorcd_summary, id_vars="Standard")
#
# lorcd_summary.columns.values[2] = "LORCD"
# lorcd_summary.columns.values[1] = "Background_Matrix"
#
# fig = px.box(lorcd_summary,
#              x="Standard",
#              y="LORCD",
#              color="Standard",
#              title="LORCD per standard across all background matrices",
#              points="all")
#
# fig.update_layout(xaxis_title = "Standard",
#                   yaxis_title = "LORCD (Limit of reproducible computational detection) (μg/mL)")
#
# fig.write_html(f"{path}LORCD_boxplots.html")


