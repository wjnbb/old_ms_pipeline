import numpy as np

from src.assign_global_variables import (
    Bio_identifier,
    Blank_identifier,
    Media_identifier,
    QC_identifier,
)


def detect_sample_groups(sample_names):

    # get all biological sample names from list of sample names
    if (len([s for s in sample_names if Bio_identifier in s])) >= 1:

        Bio = np.unique([s for s in sample_names if Bio_identifier in s]).tolist()
        print(Bio[0:10])
        print("Number of Biological samples found = " + str(len(Bio)))
        Bio_groups = np.unique([b.split("rep")[0] for b in Bio]).tolist()
        print(Bio_groups[0:10])
        print("Number of Biological groups found = " + str(len(Bio_groups)))
    else:
        Bio = []
        Bio_groups = []
        print("No biological samples present")

    # get all media sample names from list of sample names
    if (len([s for s in sample_names if Media_identifier in s])) >= 1:

        Media = np.unique([s for s in sample_names if Media_identifier in s]).tolist()
        print(Media[0:10])
        print("Number of Media samples found = " + str(len(Media)))
        Media_groups = np.unique([b.split("rep")[0] for b in Media]).tolist()
        print(Media_groups[0:10])
        print("Number of Media groups found = " + str(len(Media_groups)))

    else:
        Media = []
        Media_groups = []
        print("No Media samples present")

    # get all blank sample names from list of column names
    if (len([s for s in sample_names if Blank_identifier in s])) >= 1:

        Blanks = np.unique([s for s in sample_names if Blank_identifier in s]).tolist()
        Blanks = [b for b in Blanks if "Condition" not in b]
        print(Blanks[0:10])
        print("Number of blank samples found = " + str(len(Blanks)))
    else:
        Blanks = []
        print("No Blank samples present")

    # get all QC sample names from list of column names
    if (len([s for s in sample_names if QC_identifier in s])) >= 1:

        QCs = np.unique([s for s in sample_names if QC_identifier in s]).tolist()
        QCs = [b for b in QCs if "Condition" not in b]
        print(QCs[0:10])
        print("Number of QC samples found = " + str(len(QCs)))
    else:
        QCs = []
        print("No QC samples present")

    return Bio, Media, Blanks, QCs, Bio_groups, Media_groups
