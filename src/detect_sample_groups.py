import numpy as np

from src.assign_global_variables import (
    Bio_identifier,
    Blank_identifier,
    Media_identifier,
    QC_identifier,
)


def detect_sample_groups(sample_names: list):

    """Takes a list of sample names and detects and divides samples into biological, blank, media/control and QC sample
       groups based on the strings provided for Bio_identifier, Blank_identifier, Media_identifier, QC_identifier, and
       their presence in the sample names. Biological and Media/Control samples may be divided into further subgroups."""

    print("\nBiological sample identifier used is...." +  Bio_identifier)
    print("Media or control sample identifier used is...." + Media_identifier)
    print("Blank sample identifier used is...." + Blank_identifier)
    print("QC sample identifier used is...." + QC_identifier)
    print("")

    # get all biological sample names from list of sample names
    if (len([s for s in sample_names if Bio_identifier in s])) >= 1:

        Bio = np.unique([s for s in sample_names if Bio_identifier in s]).tolist()
        print("\nFirst ten biological samples names are...")
        print(Bio[0:9])
        print("Number of Biological samples found = " + str(len(Bio)))
        Bio_groups = np.unique([b.split("rep")[0] for b in Bio]).tolist()
        print(Bio_groups[0:10])
        print("Number of Biological groups found = " + str(len(Bio_groups)))
    else:
        Bio = []
        Bio_groups = []
        print("\nNo biological samples present")

    # get all media sample names from list of sample names
    if (len([s for s in sample_names if Media_identifier in s])) >= 1:

        Media = np.unique([s for s in sample_names if Media_identifier in s]).tolist()
        print("\nFirst ten media/control samples names are...")
        print(Media[0:9])
        print("Number of Media/control samples found = " + str(len(Media)))
        Media_groups = np.unique([b.split("rep")[0] for b in Media]).tolist()
        print(Media_groups[0:10])
        print("Number of Media groups found = " + str(len(Media_groups)))

    else:
        Media = []
        Media_groups = []
        print("\nNo Media samples present")

    # get all blank sample names from list of column names
    if (len([s for s in sample_names if Blank_identifier in s])) >= 1:

        Blanks = np.unique([s for s in sample_names if Blank_identifier in s]).tolist()
        Blanks = [b for b in Blanks if "Condition" not in b]
        print("\nFirst ten blank samples names are...")
        print(Blanks[0:9])
        print("Number of blank samples found = " + str(len(Blanks)))
    else:
        Blanks = []
        print("\nNo Blank samples present")

    # get all QC sample names from list of column names
    if (len([s for s in sample_names if QC_identifier in s])) >= 1:

        QCs = np.unique([s for s in sample_names if QC_identifier in s]).tolist()
        QCs = [b for b in QCs if "Condition" not in b]
        print("\nFirst ten QC samples names are...")
        print(QCs[0:9])
        print("Number of QC samples found = " + str(len(QCs)))
    else:
        QCs = []
        print("\nNo QC samples present")

    return Bio, Media, Blanks, QCs, Bio_groups, Media_groups
