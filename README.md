# genome_position_liftover_script
A short script to leftover genome positions between builds for use in a pipeline

## Setup
You will need an anaconda installation to setup the environemnt.yml file and use the script.
This may be available through a module system, where you should load it into your instance before starting.
eg:
> module load Anaconda

Once *anaconda* is activated, the environment should be setup using the supplied yaml file (*liftover_environment.yml*) using the following code:
> conda env create -f liftover_environment.yml

This only needs to be done once.

You can check that the environment is installed correctly using:
> conda env list

> **_NOTE_** the * indicates the active environment at the time

The script may also want to be executed from the command line, and can be changed using:
> chmod +x liftover.py

The file *liftover.py* may change colour when checking files using *ls*.

## After Setup (or everytime you want to use the program)
Ensure Anaconda is loaded:
> module load Anaconda

Activate the environment:
> conda activate liftover

The python file can then be used. For help on the command line inputs use (within teh directory the python file is in):
> ./liftover.py -h

The environment can then be deactivated for other scripts to be used using:
> conda deactivate

## Usage
### Inputs

### Outputs
