import json, pytz, argparse
from datetime import datetime


def vatspyDatToJson(inputFile, outputFile, airacCycle):


    # FIXME: Test if input filename exists


    file = open(inputFile, 'r')
    lines = file.readlines()

    # Base JSON information
    time_now = datetime.now(pytz.utc)
    time_stamp = time_now.strftime("%Y%m%d")

    general = {
        "version": "0.0.1",
        "lastUpdated": time_stamp,
        "vatspyData": "airac" + airacCycle
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
            #print("Category Change! New: " + table)  # FIXME for debugging

        # Ignore commented out lines
        elif line.startswith(';'):
            pass

        # If not a new category, or a commented line
        else:
            # Get rid of new line charcaters, and split into a list for each column
            x = line.strip()
            x = x.split("|")

            if table == "Countries":
                # Ignore empty list entries
                if len(x) == 1:
                    pass
                else:
                    countries[i] = {
                        "name": x[0],
                        "code": x[1],
                        "type": x[2]
                    }
                i += 1

            if table == "Airports":
                # Ignore empty list entries
                if len(x) == 1:
                    pass

                else:
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

                if len(x) == 1:
                    pass
                else:
                    firs[i] = {
                        "icao": x[0],
                        "name": x[1],
                        "callsignPrefix": x[2],
                        "firBoundary": x[3]
                    }

                    i += 1

            if table == "UIRs":

                if len(x) == 1:
                    pass
                else:
                    uirs[i] = {
                        "prefix": x[0],
                        "name": x[1],
                        "coverageFirs": x[2]
                    }

                    i += 1

            if table == "IDL":
                if len(x) == 1:
                    pass
                else:
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
    with open(outputFile, 'w') as outfile:
        json.dump(dictionary, outfile)

    print("Success!")
    print("AIRAC {} : Successfully converted file {}. It has been saved as {}".format(airacCycle, inputFile, outputFile))

def run():
    parser = argparse.ArgumentParser()

    # -f FILE
    parser.add_argument("-f", "--filename", help="The path to the input file", default="VATSpy.dat")
    parser.add_argument("-o", "--output", help="(Optional) Filename (and path) to the output file", default="VATSpy.json")
    parser.add_argument("-a", "--airac", help="The number of the AIRAC cycle of the VATSIM Data", required=True)

    args = parser.parse_args()

    if args.filename == False:
        print("You must specify a filename with -f. Use --help for more info.")

    vatspyDatToJson(args.filename, args.output, args.airac)
