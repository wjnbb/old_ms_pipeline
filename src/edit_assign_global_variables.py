

def edit_variables(dataset:str):

    fg_data_path = "C:/Users/WilliamNash/Bactobio Dropbox/Baccuico/LAB Work/Lab Work - Will/AC003_DataFiltering/FG_investigation_results/"
    print(dataset)

    with open("C:/Users/WilliamNash/PycharmProjects/mass-spec-pipeline/src/assign_global_variables.py", 'r') as file:
        data=file.readlines()
        data[0] = f'path = "{fg_data_path}{dataset}/"\n'
        data[1] = f'batch_name = "{dataset}"\n'
        data[3] = f'peaklist = "{dataset}.csv"\n'

    with open("C:/Users/WilliamNash/PycharmProjects/mass-spec-pipeline/src/assign_global_variables.py", 'w') as file:
        file.writelines(data)