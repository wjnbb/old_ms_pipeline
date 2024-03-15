
def ID_levels(Mods_filt: list):

    # initialise list to store results in
    ID_level = list()
    ms2_hits = []

    # loop through all features
    for i in Mods_filt[7].index:

        # check all MS2 matches to see if their score passes the minimum threshold for a confident match
        if (Mods_filt[1]).loc[i, "spectral_db_matches:cosine_score"] >= 0.7:

            # if the match score was good enough, then calculate the ppm error
            ref_mz = (Mods_filt[1]).loc[i, "spectral_db_matches:precursor_mz"]
            exp_mz = (Mods_filt[7]).loc[i, "mz"]
            ms2_ppm_error = ((exp_mz-ref_mz)/ref_mz)*1000000

            # check the ppm error is between -5 and +5 and assign as a level 2 ID if so
            if (ms2_ppm_error <= 5) & (ms2_ppm_error >= -5):

                ID_level.append("Level 2")
                ms2_hits.append(i)
                continue

            elif (((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] <= 5) &
                 ((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] >= -5)):

                ID_level.append("Level 3")
                continue

            # if the ppm error on the MS1 match was too wide check the MF prediction combined score is good to assign level 4
            elif ((Mods_filt[4]).loc[i, "ion_identities:combined_score"]) >= 0.75:

                ID_level.append("Level 4")
                continue

            else:

                # print("Recorded m/z only - assigned featureID " + str(i) + " as level 5")
                ID_level.append("Level 5")
                continue

        # if the ppm error on the MS2 match was too wide check the MS1 match is between -5 and +5 ppm
        elif(((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] <= 5) &
             ((Mods_filt[0]).loc[i, "compound_db_identity:mz_diff_ppm"] >= -5)):

            # print("MS1 ppm error was acceptable - assigned featureID " + str(i) + " as level 3")
            ID_level.append("Level 3")
            continue

        # if the ppm error on the MS1 match was too wide check the MF prediction combined score is good to assign level 4
        elif ((Mods_filt[4]).loc[i, "ion_identities:combined_score"]) >= 0.75:

            ID_level.append("Level 4")
            continue

        # assign anything which didn't meet any of the above criteria a level 5
        else:

            # print("Recorded m/z only - assigned featureID " + str(i) + " as level 5")
            ID_level.append("Level 5")
            continue

    print("")
    print(str(ID_level.count("Level 2")) + " level 2 annotations assigned")
    print(str(ID_level.count("Level 3")) + " level 3 annotations assigned")
    print(str(ID_level.count("Level 4")) + " level 4 annotations assigned")
    print(str(ID_level.count("Level 5")) + " level 5 annotations assigned")

    (Mods_filt[7]).insert(loc=0, column="Level_of_ID", value=ID_level)

    print("")
    for hit in ms2_hits:

        print(f'MS2 hit found for {((Mods_filt[1]).loc[hit,"spectral_db_matches:compound_name"])} with a match score of {((Mods_filt[1]).loc[hit, "spectral_db_matches:cosine_score"])}')

    return Mods_filt















