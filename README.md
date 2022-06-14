# genome_position_liftover_script
A short script to leftover genome positions between builds for use in a pipeline

## Setup
You will need an anaconda installation to setup the environemnt.yml file and use the script.
This may be available through a module system, where you should load it into your instance before starting.
eg:
``` module load Anaconda ```

Once *anaconda* is activated, the environment should be setup using the supplied yaml file (*liftover_environment.yml*) using the following code:

``` conda env create -f liftover_environment.yml ```

This only needs to be done once.

You can check that the environment is installed correctly using:

``` conda env list ```

> **_NOTE_** the * indicates the active environment at the time

The script may also want to be executable from the command line, and can be changed using:
``` chmod +x liftover.py ```

The file *liftover.py* may change colour when checking files using *ls*.

## After Setup (or everytime you want to use the program)
Ensure Anaconda is loaded:

``` module load Anaconda ```

Activate the environment:

``` conda activate liftover ```

The python file can then be used. For help on the command line inputs use (within teh directory the python file is in):

``` ./liftover.py -h ```

The environment should then be deactivated for other scripts to be used using:

``` conda deactivate ```

## Usage
### Inputs

| Input Name            | Flag (if available)   | About                                                                      |
|-----------------------|-----------------------|----------------------------------------------------------------------------|
| chr                   |                       | Column number of the chromosomes (0-indexed)                               |
| pos                   |                       | Column number of the positions to move over                                |
| build_from            |                       | Build number file is currently in (eg b38)                                 |
| build_to              |                       | Build number of converted file (eg hg19)                                   |
| file                  |                       | Input file (file to convert to new build)                                  |
| header                | --header / --no-header| Include --header if input file has a header (skips first row)              |
| delimiter             | --delim               | Delimiter of the input file (default is space)                             |
| delimiter (of output) | --delim_out           | Delimiter to use for the new output file (defaults to tab delimited)       |
| output file name      | --out                 | Output filename (default will be \[*build_to*]\_converted_\[*Input file*] |

### Outputs
A tab delimited file with name \[*build to*]\_converted_\[*file name*]. Eg hg39_converted_summary_statistics.txt.
Only the positions column of the file will be updated, all other columns will remain the same
