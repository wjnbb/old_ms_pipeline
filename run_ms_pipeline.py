import argparse
import configparser
import datetime
import logging
import os
import shutil
import subprocess
import sys

from src.xml_utils import prep_batch_file

# constants
BATCH_XML = "batch_file.xml"

# set logger
logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


def _extract_args():

    # input args
    parser = argparse.ArgumentParser(
        description="Processes LCMS output with MSConvert & MZMine3 to produce a peak table."
    )

    parser.add_argument(
        "-i",
        "--input_dir",
        dest="INPUT_DIR",
        action="store",
        type=str,
        required=True,
        help="Path to directory with input files",
    )

    parser.add_argument(
        "-r",
        "--run_name",
        dest="RUN_NAME",
        action="store",
        type=str,
        default=None,
        help="Optional run name. If not given, a run name with the current timestamp will be used.",
    )

    parser.add_argument(
        "-c",
        "--config_file",
        dest="CONFIG_FILE",
        action="store",
        type=str,
        default="config.ini",
        help=(
            "Ini config file with paths to metabolite db, spectral library, "
            "batch file template, pwiz singulatiry and tmpdir."
            "Example format in README. "
            "If not given, defaults to 'config.ini' in root of repo."
        ),
    )

    parser.add_argument(
        "-debug",
        dest="DEBUG",
        action="store_const",
        const=True,
        default=False,
        help="Run with debug-mode logging.",
    )

    args = parser.parse_args()

    # set logger config based on --debug command-line flag. (basicConfig is
    # design to be run only once.)
    logging.basicConfig(
        level=logging.DEBUG if args.DEBUG else logging.INFO,
        format="%(levelname)s: in '%(funcName)s' (%(filename)s): %(message)s",
    )

    return (
        args.INPUT_DIR,
        args.RUN_NAME,
        args.CONFIG_FILE,
    )


def main():
    """Driver script to run mass spec pipeline. SCIEX raw data is converted to mzXML format with msConvert
    then processed with MZmine3 to produce a peaktable.
    """

    input_dir, run_name, config_file = _extract_args()

    # read config
    config = configparser.ConfigParser()
    config.read(config_file)

    # generate new run directory in output dir
    if run_name:
        run_dir = os.path.join(config["general"]["output_dir"], run_name)
    else:
        run_dir = os.path.join(
            config["general"]["output_dir"],
            f"ms_run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )

    if not os.path.exists(run_dir):
        os.mkdir(run_dir)

    _LOGGER.info(f"Run output: {run_dir}")

    # run msconvert to generate mzXML files from wiff files
    wiff2 = [f for f in os.listdir(input_dir) if f.endswith(".wiff2")]
    if not wiff2:
        raise Exception("No wiff2 present in input files")
    wiff2 = wiff2[0]

    ms_convert_output = os.path.join(run_dir, "mzxmls")
    if not os.path.exists(ms_convert_output):
        _LOGGER.info("Running msconvert...")
        os.mkdir(ms_convert_output)

        # set input paths to bind to container
        HOST_INPUT = input_dir
        CONTAINER_INPUT = "/data/inputs"

        # set output paths to bind to container
        HOST_OUTPUT = ms_convert_output
        CONTAINER_OUTPUT = "/data/outputs"

        # set tmp path with write access to bind for wine
        # this step circumvents the need for root write access to wine within the container
        HOST_WINE = os.path.join(config["general"]["tmpdir"], "wineXXX")
        CONTAINER_WINE = "/mywineprefix"

        # get path to proteowizard sandbox directory from config
        PWIZ_SANDBOX = config["msconvert"]["pwiz_sandbox"]

        try:
            # execute singularity and bind directories
            # run msconvert command from proteowizard sandbox
            subprocess.run(
                f'singularity exec \
                    -B {HOST_INPUT}:{CONTAINER_INPUT} \
                    -B {HOST_OUTPUT}:{CONTAINER_OUTPUT} \
                    -B `mktemp -d {HOST_WINE}`:{CONTAINER_WINE} \
                    -w {PWIZ_SANDBOX} \
                    wine msconvert \
                    {CONTAINER_INPUT}{wiff2} \
                    -o {CONTAINER_OUTPUT} \
                    --mzXML \
                    --32 \
                    --filter "peakPicking vendor msLevel=1-" \
                    --ignoreUnknownInstrumentError \
                    --verbose',
                shell=True,
                check=False,
            )

            _LOGGER.info("Finished msconvert")

        except (subprocess.CalledProcessError, OSError) as e:
            _LOGGER.info(e)
            _LOGGER.info("Exiting - msonvert failed.")
            # if the step fails, remove the output directory
            # shutil can remove directories with things in them (unlike os.rmdir)
            shutil.rmtree(ms_convert_output)
            sys.exit()

    # create mzmine dir
    mzmine_dir = os.path.join(run_dir, "MZmine3")
    if not os.path.exists(mzmine_dir):
        _LOGGER.info("Preparing for MZmine3...")

        os.mkdir(mzmine_dir)

        # select input files for mzmine
        mzmine_inputs = os.listdir(ms_convert_output)

        # exclude mzXML files with 'condition' from being processed by mzmine3
        mzmine_inputs = [
            os.path.join(ms_convert_output, f)
            for f in mzmine_inputs
            if "condition" not in f
        ]

        # prep batch file
        prep_batch_file(
            template_xml=config["mzmine"]["batch_template"],
            input_mzxmls=mzmine_inputs,
            output_xml=BATCH_XML,
            output_dir=mzmine_dir,
            database_csv=config["mzmine"]["metabolite_db"],
            spectral_library_json=config["mzmine"]["spectral_lib"],
        )
        _LOGGER.info("Batch file prepped")

        # run MZMine3
        _LOGGER.info("Running MZmine3...")
        try:
            subprocess.run(
                f'MZmine \
                    -batch {os.path.join(mzmine_dir, BATCH_XML)} \
                    -temp {config["general"]["tmpdir"]}',
                shell=True,
                check=True,
            )
            _LOGGER.info("Finished MZmine3")

        except (subprocess.CalledProcessError, OSError) as e:
            _LOGGER.info(e)
            _LOGGER.info("Exiting - MZMine3 failed.")

            # if the step fails, remove the output directory
            shutil.rmtree(mzmine_dir)
            sys.exit()

    _LOGGER.info("Done!")


if __name__ == "__main__":
    main()
