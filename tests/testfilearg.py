#!/usr/bin/env python3.4

from csv import Sniffer, DictReader, DictWriter
import argparse

# Create the argument parser, and parse the command line.
parser = argparse.ArgumentParser(description="""Reads absorbance data
from a Genesys spectrophotometer at specified intervals for different
volumes of substrate in an enzyme-catalyzed reaction. The absorbances
and times are written to a CSV file for later processing.""")
parser.add_argument('-f', '--file', default='kineticdata.csv',
                    type=argparse.FileType('a+'),
                    help='''The name of the file to which CSV data will be
                    appended.''')
parser.add_argument('-c', '--column', nargs='+',
                    help='Header(s) for additional columns in the data file.')
args = parser.parse_args()

# Check to see if data file already has data
args.file.seek(0)
csvtest = args.file.read(1024)
args.file.seek(0)
# Set initial counter for reactions
lastreaction = 0
# Create dictionary for writing each row
rowdict = {}
if len(csvtest) > 0: # File contains content
    if Sniffer().has_header(csvtest): # File appears to contain a header
        csvreader = DictReader(args.file)
        fieldnames = csvreader.fieldnames
        additional = fieldnames[0:len(fieldnames)] # Make a copy
        for field in ["Reaction", "Time", "Abs"]:
            additional.remove(field)
            # Should throw exception if column doesn't exist
        # Determine number of reactions for output
        # This will also position the file object at the end of the file.
        for data in csvreader:
            lastreaction = max(lastreaction, int(data["Reaction"]))
            # Use previous values as default for new rows
            for field in additional:
                rowdict[field] = data[field]
    else: # File has content but not headers. Abort!
        raise ValueError("Existing CSV file must contain appropriate headers.")
else: # New file, create fieldnames and list of column prompts
    additional = args.column
    fieldnames = ["Reaction"] + additional + ["Time", "Abs"]
    # Use field names as initial defaults for reaction
    for field in additional:
        rowdict[field] = field
csvwriter = DictWriter(args.file, fieldnames)
# Only write header if file was empty
if len(csvtest) == 0:
    csvwriter.writeheader()

args.file.close()
        
