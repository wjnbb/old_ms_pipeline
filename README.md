# mass-spec-pipeline
***
For processing Bactobio's mass spec data.

The pipeline consists of 3 main steps:
1. Converting SCIEX WIFF files to mzXMLs with ProteoWizard msConvert
2. Processing mzXML files with MZMine3 
3. Formatting the peak table

## Running the pipeline
The pipeline is intended to run on Bactobio's `bioinformatics-individual1` server and a clone of the repo
can be found at `/mnt/Volume1/repos/mass-spec-pipeline/`. This is the production version of the pipeline
and should be kept on the `main` branch.

To nohup the pipeline:

```
nohup python run_ms_pipeline.py  \
   -i /mnt/Volume1/data/mass-spec/msconvert/inputs/<folder with wiffs> \
   -r <run name> \
   > logs/`date +"%Y%m%d%H%M%S"`.log 2>&1 &
```

Run `python run_ms_pipeline.py --help` for more information about optional arguments.

## Pipeline setup
#### Base environment setup
The base environment `ms-pipeline` should be used as the default environment for developing, 
for most python and R scripts, for running tests and for linting. 
It is also the default environment for running pytests on GitHub actions whenever PRs are raised.   

To install `ms-pipeline`, follow the setup instructions and best practices outlined in the 
[bactobio-platform](https://github.com/Baccuico/bactobio-platform) repository. 
`./scripts/install.sh` in this repo will install `ms-pipeline` instead of `bb-platform`.


#### Installing pipeline dependencies
A linux verions of **ProteoWizard msConvert** is not available so setting it up is a pain... 
ProteoWizard provides a [docker image](https://hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) 
but docker runs and outputs files as root which is problematic. It also requires root access to `/wineprefix64` 
within the container so giving a user flag to `docker run` to run it as a specific user also does not work.

The solution seems to be to build a [Singularity](https://docs.sylabs.io/guides/latest/user-guide/) sandbox directory, 
change some wine settings and create a temporary directory for wine within the sandbox. 

The steps for setting up msconvert are therefore as follows:
1. Install [SingularityCE](https://docs.sylabs.io/guides/3.1/user-guide/installation.html) 
and [Go](https://go.dev/doc/install). 
Currently, [SingularityCE 3.11.0](https://github.com/sylabs/singularity/releases/tag/v3.11.0) is being used.


2. Set up the `pwiz_sandbox` as described
[here](https://github.com/jspaezp/elfragmentador-data#setting-up-msconvert-on-singularity-),
except it doesn't have to be built locally first so the tar & transfer step can be skipped. 
Also, note that `/dev/shm/` is just a common linux temp directory so change this to any writeable temp directory with lots of space.
On the `bioinformatics-individual1` server, the sandbox can be found here: ```/mnt/Volume1/tools/pwiz_singularity/pwiz_sandbox```


3. Make input and output directories in the sandbox, so we can mount different directories as inputs and outputs. E.g.:
    ```
   mkdir <path_to_sandboz_folder>/pwiz_sandbox/data/inputs
   mkdir <path_to_sandboz_folder>/pwiz_sandbox/data/outputs
   ```

Threads discussing how to run msConvert with Singularity can also be found 
[here](https://github.com/ProteoWizard/container/issues/1) and
[here](https://github.com/ProteoWizard/pwiz/issues/2387#issuecomment-1320984700).

To install **MZMine3**, download the `MZmine_Linux_portable_3.3.0` version from 
[latest releases](https://github.com/mzmine/mzmine3/releases/tag/v3.3.0), unzip, then export the path. 
On the bioinformatics-individual1 server, it is in `/mnt/Volume1/tools/`.
```
 cd /mnt/Volume1/tools/
 wget https://github.com/mzmine/mzmine3/releases/download/v3.3.0/MZmine_Linux_portable_3.3.0.zip
 unzip MZmine_Linux_portable_3.3.0.zip
 rm MZmine_Linux_portable_3.3.0.zip
 export PATH=$PATH:/mnt/Volume1/tools/MZmine_Linux_portable_3.3.0/bin/MZmine
```
To run **MZMine3** via command line, a custom xml batch file containing information about the modules and parameters 
to run is required. Template batch files were made in the GUI and can be found in 
```/mnt/Volume1/data/mass-spec/mzmine3/batch_files```. The batch file also has to include paths to 
a large spectral library databases (currently 17GB), a metabolite database and the paths to the input mzXML files.
Before running the pipeline, the databases must be provided and the paths to the databases need to be set in the config 
file as described below. The pipeline will add these, as well as mzXMLs in the input directory, to the batch file.

#### Setting pipeline configurations
The following paths must be set in a config file upon setup:
- A temporary directory with lots of space (likely the same one as for the msconvert setup)
- Run output directory
- ProteoWizard singularity sandbox
- Batch file template for MZMine3
- Metabolite database csv for MZMine3
- Spectral library json for MZMine3

By default, the pipeline will look for a `config.ini` file in the root directory of the repo, 
but any local ini-style file with the following sections and items can be given to the `--config_file` flag.
```
[general]
tmpdir = /path/to/large/writeable/tmp
output_dir = /where/to/output/result/dir

[msconvert]
pwiz_sandbox = /path/to/configured/pwiz_sandbox

[mzmine]
batch_template = /path/to/batch_files/chosen_template_batch_file.xml
metabolite_db = /path/to/databases/Metabolite_Database_v5.2_FOR_MZMINE3.csv
spectral_lib = /path/to/databases/MoNA-export-All_Spectra.json
```


## Contributing to the pipeline

#### General good practices

The aim is to create pipelines that can function as stand-alone bioinformatics tools 
and that can be deployed on any linux server.

As such, the following guidelines should be followed:
- Data should be stored outside the repo and code should be written to accept file paths or use a config file. 
- Paths to data should not be hardcoded. On the bioinformatics server, any required databases or shared data for testing 
can be stored in `/mnt/Volume1/data/mass-spec/`.
- The pipeline should not interact directly with SQL.
- Lint & test code where possible.
- Dependencies, environments and installation of external tools should be documented.
- To add dependencies to `ms-pipeline`, follow the same approach described in the 
[bactobio-platform](https://github.com/Baccuico/bactobio-platform). Additionally, while the pipeline can be built 
with the intention of only ever being run on linux, for development purposes if a dependency *only* works on linux 
it should probably have its own conda environment/ setup. 

**Developing on the server**

To work on the pipeline on a share server, please clone your own version of the repo in your personal folder
(e.g. in `/mnt/Volume1/<user>/`). This is necessary to allow multiple people to work on the server at the same time because 
checking out a branch in one copy of the repo on the server will check it out for everyone. 

**Adding command line tools**

When possible, external command-line bioinformatics tools should have their own conda environment with an associated yaml file. 
Ideally these should be activated and run through SnakeMake or other workflow management tools so that additional 
conda environments (other than the base environment) do not have to be manually set up or activated by users.

Some open source bioinformatics tools are not available on conda (or are buggy) and have to be downloaded. 
Shared tools on the bioinformatics server should be stored in `/mnt/Volume1/tools/` and if used in a pipeline should 
either require the path to the tool to be set in a config file or come with instructions to export the path to a
users `.bashrc`. In these cases, the version and download link should also be included in the pipeline documentation.
