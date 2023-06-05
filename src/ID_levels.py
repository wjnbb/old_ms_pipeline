
def ID_levels(Mods_filt: list):

    #initialise list to store results in
    ID_level = list()

    #loop through all features
    for i in Mods_filt[7].index:

        #print("\nWorking on row ID " + str(i))

        # check all MS2 matches to see if their score passes the minimum threshold for a confident match
        if((Mods_filt[1]).loc[i, "spectral_db_matches:cosine_score"] >= 0.7):

            #print("Good spectral match found")

            #if the match score was good enough, then calculate the ppm error
            ref_mz = (Mods_filt[1]).loc[i, "spectral_db_matches:precursor_mz"]
            exp_mz = (Mods_filt[7]).loc[i, "mz"]
            ms2_ppm_error = ((exp_mz-ref_mz)/ref_mz)*1000000

            #print("ms2 ppm error is " + str(ms2_ppm_error))

            #check the ppm error is between -5 and +5 and assign as a level 2 ID if so
            if((ms2_ppm_error <= 5) & (ms2_ppm_error >= -5)):

                #print("MS2 ppm error was acceptable - assigned featureID " + str(i) + " as level 2")
                ID_level.append("Level 2")
                continue

            elif((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] <= 5) & ((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] >= -5):

                #print("MS1 ppm error was acceptable - assigned featureID " + str(i) + " as level 3")
                ID_level.append("Level 3")
                continue

            # if the ppm error on the MS1 match was too wide check the MF prediction combined score is good to assign level 4
            elif((Mods_filt[2]).loc[i, "formulas:combined_score"]) >= 0.75:

                #print("MF prediction score was acceptable - assigned featureID " + str(i) + " as level 4")
                ID_level.append("Level 4")
                continue

            else:

                #print("Recorded m/z only - assigned featureID " + str(i) + " as level 5")
                ID_level.append("Level 5")
                continue

        # if the ppm error on the MS2 match was too wide check the MS1 match is between -5 and +5 ppm
        elif((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] <= 5) & ((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] >= -5):

            #print("MS1 ppm error was acceptable - assigned featureID " + str(i) + " as level 3")
            ID_level.append("Level 3")
            continue

        #if the ppm error on the MS1 match was too wide check the MF prediction combined score is good to assign level 4
        elif((Mods_filt[2]).loc[i, "formulas:combined_score"]) >= 0.75:

            #print("MF prediction score was acceptable - assigned featureID " + str(i) + " as level 4")
            ID_level.append("Level 4")
            continue

        #assign anything which didn't meet any of the above criteria a level 5
        else:

            #print("Recorded m/z only - assigned featureID " + str(i) + " as level 5")
            ID_level.append("Level 5")
            continue

    ID_level

    print("")
    print(str(ID_level.count("Level 2")) + " level 2 annotations assigned")
    print(str(ID_level.count("Level 3")) + " level 3 annotations assigned")
    print(str(ID_level.count("Level 4")) + " level 4 annotations assigned")
    print(str(ID_level.count("Level 5")) + " level 5 annotations assigned")

    (Mods_filt[7]).insert(loc=0, column="Level_of_ID", value=ID_level)

    return Mods_filt















