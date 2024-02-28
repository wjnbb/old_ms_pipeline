#This workflow includes all four main sample types
# Bio and Media (Blanks)
# Media/Blank Subtraction implemented

import os
#get the list of datasets to analyse
path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/FG_investigation_results/"
os.chdir(path)
dataset = os.listdir(path)[64]

fg_data_path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/FG_investigation_results/"
print(dataset)

with open("C:/Users/WilliamNash/PycharmProjects/mass-spec-pipeline/src/assign_global_variables.py", 'r') as file:
    data = file.readlines()
    data[0] = f'path = "{fg_data_path}{dataset}/"\n'
    data[1] = f'batch_name = "{dataset}"\n'
    data[3] = f'peaklist = "{dataset}.csv"\n'

with open("C:/Users/WilliamNash/PycharmProjects/mass-spec-pipeline/src/assign_global_variables.py", 'w') as file:
    file.writelines(data)

from src.complete_fg_workflow import complete_fg_workflow

complete_fg_workflow(dataset)





