import pandas as pd

from src.assign_global_variables import Bio_identifier, bio_media_linkers

def FC_MultiBio_vs_MultiControl(
    Bio_groups: list, Bio_stats: pd.DataFrame, Media_stats: pd.DataFrame
) -> pd.DataFrame:

    """Takes a list of multiple biological sample groups, the average peak height stats for biological sample groups and
    media/control sample group as separate Pandas dataframes. The supplied bio_media_linkers list ensures linking of the
    correct biological group to the relevant media/control group. Returns a Pandas dataframe of the fold changes for the
    multiple biological groups average peak height vs the partner control/media group average peak height."""

    ################################################################################
    # CALCULATE FC FOR EACH BIOLOGICAL WELL VS ITS MEDIA CONTROL
    # get character strings to allow pairing of relevant biological and media samples
    bio_media_pairs = [b.split(Bio_identifier)[1] for b in Bio_groups]
    FC_table = pd.DataFrame()

    #Fill the nans with 10s to ensure no nans in the FC output table
    Bio_stats = Bio_stats[[s for s in Bio_stats.columns if "avg" in s]].fillna(10)
    Media_stats = Media_stats[[s for s in Media_stats.columns if "avg" in s]].fillna(10)

    if(bio_media_linkers == "NA"):

        # calculate FC
        for b in bio_media_pairs:

            bios = [s for s in Bio_stats.columns if b in s]
            bios = [s for s in bios if "avg" in s]
            bios = Bio_stats[bios].squeeze()

            medias = [i for i in Media_stats.columns if b in i]
            medias = [i for i in medias if "avg" in i]
            medias = Media_stats[medias].squeeze()

            FC = bios / medias

            FC_table.insert(0, ("FC" + b), FC)

        return FC_table

    else:

        # calculate FC
        for b in bio_media_pairs:

            bios = [s for s in Bio_stats.columns if b in s]

            bios = [s for s in bios if "avg" in s]
            bios = Bio_stats[bios].squeeze()

            medias = [i for i in Media_stats.columns if b in i]

            if len(medias) == 0:

                for L in bio_media_linkers:

                    if L in b:

                        medias = [i for i in Media_stats.columns if L in i]
                        medias = [i for i in medias if "avg" in i]
                        medias = Media_stats[medias].squeeze()

                        FC = bios / medias

                        FC_table.insert(0, ("FC" + b), FC)

            else:

                medias = [i for i in medias if "avg" in i]
                medias = Media_stats[medias].squeeze()

                FC = bios / medias

                FC_table.insert(0, ("FC" + b), FC)

        return FC_table


def FC_MultiBio_vs_SingleControl(
    Bio_groups: list, Bio_stats: pd.DataFrame, Control_stats: pd.DataFrame
) -> pd.DataFrame:

    """Takes a list of multiple biological sample groups, the average peak height stats for biological sample groups and
    media/control sample group as separate Pandas dataframes. Returns a Pandas dataframe of the fold changes for the
    multiple biological groups average peak height vs the single control/media group average peak height."""
    ################################################################################
    # CALCULATE FC FOR EACH BIOLOGICAL WELL VS ITS MEDIA CONTROL
    # get character strings to allow pairing of relevant biological and media samples
    FC_table = pd.DataFrame()

    # Fill the nans with 10s to ensure no nans in the FC output table
    Bio_stats = Bio_stats[[s for s in Bio_stats.columns if "avg" in s]].fillna(10)
    Control_stats = Control_stats[[s for s in Control_stats.columns if "avg" in s]].fillna(10)

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

def FC_SingleBio_vs_SingleControl(
    Bio_stats: pd.DataFrame, Media_stats: pd.DataFrame, BG_ignore: str
) -> pd.DataFrame:

    """Takes a Pandas dataframe of the biological sample group peak height stats and another of the media/control group peak
    height stats. Returns a Pandas dataframe of the FC of the average biological sample peak height vs the average
    media/control sample peak height."""

    ################################################################################
    # CALCULATE FC for a single biological group vs a single media/control group
    FC_table = pd.DataFrame()

    # Fill the nans with 10s to ensure no nans in the FC output table
    Bio_stats = Bio_stats[[s for s in Bio_stats.columns if "avg" in s]].fillna(10)
    Media_stats = Media_stats[[s for s in Media_stats.columns if "avg" in s]].fillna(10)

    bios = Bio_stats

    if len([s for s in Bio_stats.columns if BG_ignore in s]) >= 1:

        bios.drop([s for s in Bio_stats.columns if BG_ignore in s], axis=1, inplace=True)

    bios = Bio_stats.iloc[:, 0]
    medias = Media_stats.iloc[:, 0]

    FC = bios / medias

    FC_table.insert(0, "FC", FC)

    return FC_table
