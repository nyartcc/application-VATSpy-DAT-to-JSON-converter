# VATSpy .DAT to .json converter

## Background
VATSIM provides a lot of useful aviation data through the VATSIM data project - an extention of the VATSPY data format designed by Ross Carlson many years ago. 
Unfortunately, this format of this file can be extremely annoying to work with as the way it breaks down data is not commonly used in a lot of programming languages.

When we wanted to use the project as a data source, we recognized that the main `VATSpy.dat` file was so annoying to work with, that we wanted to convert it to a more usable JSON format and this tool is the result.

## Requirements
This tool is built in, and requires Python 3.9 and PIP to be work. It comes with an installer, allowing you to run it easily from your own machine.

Note, this is a commandline tool, and has no GUI.

## Usage
* Download the release, or clone this repo to your local machine.
* Download the latest .dat source file from the [data project](https://github.com/vatsimnetwork/vatspy-data-project) and place it in the same folder as the script.
* Using your CLI, navigate to the downloaded folder.
* Run:
```python
pip install -e .
```

This will use `pip` to install the script to your PATH.

Once installed, you may now run the script using:
```bash
vatspy_dat_converter -a [current airac cycle]

Example:
vatspy_dat_converter -a 2202
```

### Optional Arguments
The script supports the following arguments:
```bash
(required) -a or --airac: enter the current airac cycle number for the release
(optional) -f or --filename: enter the name OR FULL PATH of the input file. Default: "VATSpy.dat"
(optional) -o or --output: enter a custom output filename. Default: "VATSpy.json" 
```


