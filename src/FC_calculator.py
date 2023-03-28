import pandas as pd

from assign_global_variables import Bio_identifier, Media_identifier


def FC_MultiBio_vs_MultiControl(Bio_groups, Bio_stats, Media_stats):

    ################################################################################
    # CALCULATE FC FOR EACH BIOLOGICAL WELL VS ITS MEDIA CONTROL
    # get character strings to allow pairing of relevant biological and media samples
    bio_media_pairs = [b.split(Bio_identifier)[1] for b in Bio_groups]
    FC_table = pd.DataFrame()

    # calculate FC
    for b in bio_media_pairs:

        bios = [s for s in Bio_stats.columns if b in s]
        bios = [s for s in bios if "avg" in s]
        bios = Bio_stats[bios].squeeze()

        medias = [i for i in Media_stats.columns if b in i]
        medias = [i for i in medias if "avg" in i]
        medias = Media_stats[medias].squeeze()

        FC = bios / medias
        print(FC[0:10])

        FC_table.insert(0, ("FC" + b), FC)

    return FC_table


def FC_MultiBio_vs_SingleControl(Bio_groups, Bio_stats, Control_stats):
    ################################################################################
    # CALCULATE FC FOR EACH BIOLOGICAL WELL VS ITS MEDIA CONTROL
    # get character strings to allow pairing of relevant biological and media samples
    FC_table = pd.DataFrame()

    # calculate FC
    for b in Bio_groups:

        bios = [s for s in Bio_stats.columns if b in s]
        bios = [s for s in bios if "avg" in s]
        bios = Bio_stats[bios].squeeze()

        control = [i for i in Control_stats.columns if "avg" in i]
        control_col = Control_stats[control].squeeze()

        FC = bios / control_col

        FC_table.insert(0, ("FC_" + b), FC)

    return FC_table


def FC_SingleBio_vs_SingleControl(Bio_stats, Media_stats):

    ################################################################################
    # CALCULATE FC for a single biological group vs a single media/control group
    FC_table = pd.DataFrame()

    bios = Bio_stats.iloc[:, 2]
    medias = Media_stats.iloc[:, 2]

    FC = bios / medias

    FC_table.insert(0, "FC", FC)

    return FC_table
