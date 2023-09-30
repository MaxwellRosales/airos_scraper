# airos_scraper

The purpose of this file is to scrape data off of the airos 8 webpage created when trying to connect to the ubiquiti radios.

This program was designed to work on a Windows Powershell Environment (Although hopefully the software moves over to Linux in the future)

To start, clone the repo, open a Powershell terminal, and then `cd` into the directory where the repo is cloned.

## Dependencies
Ensure that Python3 is installed and pip is updated by entering the following into Powershell:

`python3 -m pip install --upgrade pip`

To install webscraper dependencies, ensure you are in the project repo and type the following:

`pip3 install -r requirements.txt`

## System Parameters
Change lines 9-10 to match the desired variables
```
# SYSTEM PARAMETERS
IP                     = '192.168.1.20'
USERNAME               = 'GO'
PASSWORD               = 'BLUE'
LOGGING_FILENAME       = "signal_log.txt"
RECORDING_FREQUENCY_HZ = 1
```

`LOGGING_FILENAME` is the name of the log file that will be generated in the same directory as `scraper.py`

`RECORDING_FREQUENCY_HZ` is the number of data entries per second that will be generated.
