import pandas as pd
import plotly.express as px

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230816_SST_collision_energies/Match_Scores2.csv"

MS2_scores = pd.read_csv(path)

plot = px.violin(MS2_scores, x=MS2_scores["Strain"], y=MS2_scores["Match Scores"], color=MS2_scores['CE'], points="all")
plot.write_html("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230816_SST_collision_energies/violins.html")

plot = px.box(MS2_scores, x=MS2_scores["Strain"], y=MS2_scores["Match Scores"], color=MS2_scores['CE'], points="all")
plot.write_html("C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Mass_spec_data/20230816_SST_collision_energies/box_plot.html")

path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/Agilent_Method_Development/MS_results/MS2_opt_results_summary_CE.csv"