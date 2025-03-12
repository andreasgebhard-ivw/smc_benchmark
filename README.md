# smc_benchmark

## How to use

### Download the repository
 
Download as ZIP by navigating to *Code > Download  ZIP*
 
Or download using git:
 
```
git clone https://github.com/FAST-LB/smc_benchmark.git
```
### Install the Python package
 
Navigate to the folder
 
```
cd smc_benchmark
```
 
and install the package with
 
```
python -m pip install .
python install/download_sam.py
```

## Scripts

The folder `scripts` contains CLI scripts to `smc_benchmark`'s core functionalities.
Using these, the main workflows for processing csv and image data can be realized as follows.

## Image processing workflow
The image processing workflow comprises three substeps:

1. Rename files
2. Reformat files
3. Sort files

