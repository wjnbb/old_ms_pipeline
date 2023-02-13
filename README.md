# mass-spec-pipeline
Pipeline for processing mass spec data.

## Pipeline setup
Follow the setup instructions and best practices outlined in the 
[bactobio-platform](https://github.com/Baccuico/bactobio-platform) repository.

`./scripts/.install.sh` will install the `ms-pipeline` conda environment which should be used as the base environment 
for most python and R scripts, for running tests and for linting. It is also the default environment for running pytests
on GitHub actions whenever PRs are raised.

## Running the pipeline
The pipeline is intended to run on Bactobio's `bioinformatics-individual1` server and a clone of the repo
can be found at `/mnt/Volume1/repos/mass-spec-pipeline/`. This is the production version of the pipeline
and should be kept on the `main` branch.

Steps for running the pipeline to come...

## Contributing to the pipeline

**General good practices**

The aim is to create pipelines that can function as stand-alone bioinformatics tools and that can be deployed on any server.
As such, the following guidelines should be followed:
- Data should be stored outside the repo and code should be written to accept file paths or use a config file. 
Paths to data should not be hardcoded. On the bioinformatics server, any required databases or shared data for testing 
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
