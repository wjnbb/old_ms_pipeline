import os
import xml.etree.ElementTree as ET
from typing import Union

_INPUT_ELEMENT = './/parameter[@name="File names"]'
_INPUT_TAG = "file"

_DB_ELEMENT = './/parameter[@name="Database file"]'
_DB_TAG = "current_file"

_PEAK_FILE_ELEMENT = './/batchstep[@method="io.github.mzmine.modules.io.export_features_csv.CSVExportModularModule"].//parameter[@name="Filename"]'
_PEAK_FILE_TAG = "current_file"

_PROJECT_FILE_ELEMENT = './/parameter[@name="Project file"]'
_PROJECT_FILE_TAG = "current_file"

_JSON_ELEMENT = './/parameter[@name="Spectral library files"]'
_JSON_TAG = "file"

_GNPS_OUTPUT_ELEMENT = './/batchstep[@method="io.github.mzmine.modules.io.export_features_gnps.fbmn.GnpsFbmnExportAndSubmitModule"].//parameter[@name="Filename"]'
_GNPS_OUTPUT_TAG = "current_file"


def _set_xml_filepaths(
    root: ET.Element,
    elem_identifier: str,
    tag_name: str,
    files_to_add: Union[list, str],
):

    """Removes any existing children then adds filepaths to an element in xml tree."""

    # nest within list if single file given
    if isinstance(files_to_add, str):
        files_to_add = [files_to_add]

    # pull out element to edit
    elem = root.find(elem_identifier)

    # remove existing files in reverse order (otherwise iteration gets weird)
    for e in elem[::-1]:
        elem.remove(e)

    # add new files
    for f in files_to_add:
        ET.SubElement(elem, tag_name).text = f


def prep_batch_file(
    template_xml: str,
    input_mzxmls: list,
    output_xml: str,
    output_dir: str,
    database_csv: str,
    spectral_library_json: str,
):

    """Creates xml batch file for MZMine3 from template and sets filepaths.
    Input files and output directory are required, database & json files are optional.
    """

    # read in template
    tree = ET.parse(template_xml)
    root = tree.getroot()

    # set input files
    _set_xml_filepaths(root, _INPUT_ELEMENT, _INPUT_TAG, input_mzxmls)

    # set output files
    peak_file = [os.path.join(output_dir, "peaklist.csv")]
    project_file = [os.path.join(output_dir, "mzmine3_project.mzmine")]
    gnps_output = [os.path.join(output_dir, "GNPS_FBMN")]

    # set peak file
    _set_xml_filepaths(root, _PEAK_FILE_ELEMENT, _PEAK_FILE_TAG, peak_file)

    # set project file
    _set_xml_filepaths(root, _PROJECT_FILE_ELEMENT, _PROJECT_FILE_TAG, project_file)

    # set gnps output file
    _set_xml_filepaths(root, _GNPS_OUTPUT_ELEMENT, _GNPS_OUTPUT_TAG, gnps_output)

    # set bactobio database is if given
    _set_xml_filepaths(root, _DB_ELEMENT, _DB_TAG, database_csv)

    # set json database if given
    _set_xml_filepaths(root, _JSON_ELEMENT, _JSON_TAG, spectral_library_json)

    # write output
    tree.write(os.path.join(output_dir, output_xml))
