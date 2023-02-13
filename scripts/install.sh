#!/bin/bash
set -euo pipefail # https://gist.github.com/vncsna/64825d5609c146e80de8b1fd623011ca
DIR=$(dirname ${BASH_SOURCE[0]})
cd "$DIR"/..

# flags
CONDA=$(which conda || true)
cflg=0
while getopts 's:c' opt; do
    case $opt in
        # if "s" flag is specified, uses a specifc conda
        # useful on a server environment
        (s)     CONDA=${OPTARG};;

    esac
done

# hardcode conda environment
CONDA_ENV="ms-pipeline"

# only build if conda is installed
if [[ -z ${CONDA} ]]; then
    echo 'Aborting setup: Make sure conda is installed See https://docs.conda.io/en/latest/miniconda.html'
    echo 'If conda is already installed, try re-running install script from the base conda environment.'
    exit 0
fi

DEPS="--file requirements.txt --file requirements-R.txt"
CHANNELS="-c conda-forge -c defaults"

# install 
echo '(Re)installing dependencies...'
${CONDA} list -n "$CONDA_ENV" &>/dev/null || ${CONDA} create -y -n "$CONDA_ENV"
${CONDA} install -n "$CONDA_ENV" --strict-channel-priority $CHANNELS -Syq $DEPS

echo 'Dependencies install finished.'

