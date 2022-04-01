import json, pytz, argparse
import os
import sys
from datetime import datetime

import requests

verbose = True
debug = True

DAT_FILE_NAME = 'VATSpy.dat'
JSON_FILE_NAME = 'VATSpy.json'
META_NAME = 'VATSpy.meta'
release_tag = ""


# Check if the file exists
def check_file(file_name):
    if verbose:
        print("Checking if file exists")
    try:
        with open(file_name):
            return True
    except FileNotFoundError:
        return False


# Check the first line of the metadata file
def check_metadata(file_name):
    if verbose:
        print("Checking metadata")
    try:
        check_file(file_name)

        with open(file_name) as f:
            first_line = f.readline()
            return first_line
    except FileNotFoundError:
        return ""


def download_vatspy_data():
    """
    Download the latest navdata from the VATSpy Data Project Github Repo and save it to the current directory as
    a .dat file. Also stores a .meta file containing the current release_tag for easier comparison.
    :return: True if successful, False otherwise
    """
    # Download the latest navdata file
    # Check the file exists
    REPO_URL = "https://api.github.com/repos/vatsimnetwork/vatspy-data-project/releases/latest"

    d = {}
    r = requests.get(REPO_URL)  # Get the latest release
    asset = r.json()

    # Compare the current version to the latest release
    current_version = check_metadata(META_NAME)
    latest_version = asset['tag_name']
    print("Current version: " + current_version)
    print("Latest version: " + latest_version)

    global release_tag
    release_tag = asset["tag_name"]

    if current_version == latest_version:
        print("No new version available")  # No new version available
    else:
        print("New version available! \n Version: {} \n Published at: {}".format(release_tag, asset[
            "published_at"]))  # New version available

        user_accept = input("Download new version? (y/n) ")
        if user_accept == "y":

            print("Downloading latest version...")

            for i in asset["assets"]:
                if i["name"] == DAT_FILE_NAME:
                    d["url"] = i["browser_download_url"]  # Get the URL of the latest VATSpy.dat
            if verbose:
                print("tag_name:", asset["tag_name"])
                print("d:", d)

            download_url = d["url"]
            if verbose:
                print("download_url:", download_url)

            r = requests.get(download_url)  # Download the VATSpy.dat file
            with open(DAT_FILE_NAME, "wb") as f:
                f.write(r.content)  # Write the file to the current directory
            with open(META_NAME, "w") as f:
                f.write(asset["tag_name"])  # Write the tag_name to the current directory
            print("Downloaded {}".format(DAT_FILE_NAME))  # Print to the CLI
            return True
        else:
            print("No new version downloaded")
            return Exception


def vatspy_dat_to_json():
    """
    Converts the DAT file to JSON
    :return: True/False if the conversion succeeded or not. Will print to the CLI as well.
    """

    # Get the latest AIRAC cycle and create a .dat file for it.
    try:
        download_vatspy_data()  # Download the latest VATSpy.dat file from the VATSpy Data Project Github Repo.
    except Exception as e:
        print("Error downloading VATSpy.dat")
        return False

    try:
        with open(DAT_FILE_NAME, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("The file specified does not exist.")

    # Base JSON information
    time_now = datetime.now(pytz.utc)
    time_stamp = time_now.strftime("%Y%m%d")

    general = {
        0: {
            "lastUpdated": time_stamp,
            "vatspyData": release_tag
        },
    }

    # Initialize counters
    i = 0
    table = ""

    # Initialize a bunch of empty dictionaries
    countries = {
    }

    airports = {
    }

    firs = {
    }

    uirs = {
    }

    idl = {
    }

    # Loop through the input file, line by line
    for line in lines:

        # Check for a new category, ex: [Countries]
        if line.startswith('[') & line.endswith(']\n'):
            table = line[1:-2]

            # Reset the counter
            i = 0
            if verbose:
                print("Category Change! New: " + table)

        # Ignore commented out lines
        elif line.startswith(';'):
            pass

        # If not a new category, or a commented line
        else:
            # Get rid of new line characters, and split into a list for each column
            x = line.strip()
            x = x.split("|")

            if table == "Countries":
                # Ignore empty list entries
                if len(x) != 1:
                    countries[i] = {
                        "name": x[0],
                        "code": x[1],
                        "type": x[2]
                    }
                i += 1

            if table == "Airports":
                # Ignore empty list entries
                if len(x) != 1:
                    airports[i] = {
                        "icao": x[0],
                        "name": x[1],
                        "latitude": x[2],
                        "longitude": x[3],
                        "iata": x[4],
                        "fir": x[5],
                        "isPseudo": x[6]
                    }

                    i += 1

            if table == "FIRs":

                if len(x) != 1:
                    firs[i] = {
                        "icao": x[0],
                        "name": x[1],
                        "callsignPrefix": x[2],
                        "firBoundary": x[3]
                    }

                    i += 1

            if table == "UIRs":

                if len(x) != 1:
                    uirs[i] = {
                        "prefix": x[0],
                        "name": x[1],
                        "coverageFirs": x[2]
                    }

                    i += 1

            if table == "IDL":
                if len(x) != 1:
                    idl[i] = {
                        "cord1": x[0],
                        "cord2": x[1]
                    }
                    i += 1

    # Build a dictionary of all the dictionaries
    dictionary = {
        "general": general,
        "countries": countries,
        "airports": airports,
        "firs": firs,
        "uirs": uirs,
        "idl": idl
    }

    # Dump it to JSON and save it as a file.
    with open(JSON_FILE_NAME, 'w') as outfile:
        json.dump(dictionary, outfile)

    print("Success!")
    print(
        "AIRAC {} : Successfully converted file {}. It has been saved as {}".format(release_tag, DAT_FILE_NAME,
                                                                                    JSON_FILE_NAME))
    return True


def run():
    convert = vatspy_dat_to_json()
    if convert:
        print("Success!")


if __name__ == "__main__":
    run()
