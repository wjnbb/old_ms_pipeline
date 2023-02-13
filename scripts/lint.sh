#!/bin/bash
set -euo pipefail # https://gist.github.com/vncsna/64825d5609c146e80de8b1fd623011ca
DIR=$(dirname ${BASH_SOURCE[0]})
cd "$DIR"/..

echo 'sorting imports...'
isort .

echo 'linting python...'
black .

echo 'linting R...'
Rscript -e 'styler::style_dir()' 
