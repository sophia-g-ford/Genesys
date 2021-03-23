#!/usr/bin/env python3.4

# Hello world

# This program uses an interface with the Genesys spectrophotometer to
# collect timecourse data for enzyme-catalyzed reactions using different
# volumes of substrate. The absorbance, time elapsed and volume of substrate
# will be written to a CSV file that can be read into another program
# for processing. Future versions may calculate slopes and write these
# slopes into the CSV file.

from genesys import Genesys
from datetime import datetime
from csv import Sniffer, DictReader, DictWriter
from time import sleep
import argparse
from matplotlib import pyplot
from scipy.stats import linregress

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
 
class Window(QMainWindow):
   def init(self):
       super().init()
 
       self.setGeometry(300, 300, 600, 400)
       self.setWindowTitle("PyQt5 window")
       self.show()
 
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())

# Create a reference to the datetime.now function to simplify later code.
now = datetime.now

# Create the argument parser, and parse the command line.
parser = argparse.ArgumentParser(description="""Reads absorbance data
from a Genesys spectrophotometer at specified intervals for different
volumes of substrate in an enzyme-catalyzed reaction. The absorbances
and times are written to a CSV file for later processing.""")
parser.add_argument('-s', '--serial', default='/dev/ttyUSB0',
                    help='The serial port to which the device is attached.')
parser.add_argument('-f', '--file', default='kineticdata.csv',
                    type=argparse.FileType('a+'),
                    help='''The name of the file to which CSV data will be
                    appended.''')
parser.add_argument('-w', '--wave', type=int,
                    help='The wavelength at which to record absorbances.')
parser.add_argument('--freq', type=float, default=1,
                    help='The number of seconds to wait between readings.')
parser.add_argument('-t', '--time', type=float, default=120,
                    help='The duration of each timecourse in seconds.')
parser.add_argument('-b', '--blank', action='store_true',
                    help='''If the program should blank the machine before
                    each timecourse.''')
parser.add_argument('--beep', nargs='?', choices=range(1,4), const=3,
                    help='The number of times to beep after a run is completed.')
parser.add_argument('-c', '--columns', nargs='+', default=[],
                    help='Header(s) for additional columns in the data file.')
matplot = parser.add_mutually_exclusive_group()
matplot.add_argument('-p', '--plot', action='store_true',
                    help='''Plot the absorbance as a function of time after
                    each timecourse.''')
matplot.add_argument('--slope', metavar='COLUMN',
                    help='''Store the slope of the line of best fit to the
                    absorbance as a function of time, instead of the
                    individual time points. At the end of each reaction, plot
                    the slope as a function of the number in COLUMN for each
                    of the reactions performed during this session.''')
args = parser.parse_args()

# Check to see if data file already has data
args.file.seek(0)
csvtest = args.file.read(1024)
args.file.seek(0)
# Set initial counter for reactions
lastreaction = 0
# Determine which column headers will be needed for this file.
if args.slope is not None:
    endheaders = ["Slope", "Slope.Err"]
    # Might as well also create lists for data
    slopelist = []
    xvarlist = []
else:
    endheaders = ["Time", "Abs"]
# Create dictionary for writing each row
rowdict = {}
if len(csvtest) > 0: # File contains content
    if Sniffer().has_header(csvtest): # File appears to contain a header
        csvreader = DictReader(args.file)
        fieldnames = csvreader.fieldnames
        additional = fieldnames[0:len(fieldnames)] # Make a copy
        for field in ["Reaction"] + endheaders:
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
    additional = args.columns
    fieldnames = ["Reaction"] + additional + endheaders
    # Use field names as initial defaults for reaction
    for field in additional:
        rowdict[field] = field
csvwriter = DictWriter(args.file, fieldnames, extrasaction='ignore')
# Only write header if file was empty
if len(csvtest) == 0:
    csvwriter.writeheader()
# Check that args.slope will actually be in the dictionary
if args.slope is not None:
    if args.slope not in fieldnames:
        raise ValueError('Slope must be one of the headers in CSV file.')

# Initialize spectrometer
spec20 = Genesys(args.serial)
if args.wave is not None:
    spec20.wavelength(args.wave)
    if not args.blank:
        # Only prompt for initial blank if wavelength has been changed by
        # program and blanking will not be done before every reaction.
        input('Place reference cuvette in holder and press Enter:')
        spec20.blank()

# Start reaction loop. Break when user doesn't agree to another reaction. 
while True:
    lastreaction = lastreaction + 1
    rowdict["Reaction"] = lastreaction
    for field in additional:
        newvalue = input("{0} (Default: {1}): ".format(field, rowdict[field]))
        if newvalue != "":
            rowdict[field] = newvalue
    if args.blank:
        input("Place reference cuvette into holder and press Enter")
        spec20.blank()
    if args.plot or (args.slope is not None):
        timelist = []
        abslist = []
    input("Place initiated reaction cuvette in holder and press Enter")
    starttime = now()
    while True:
        sleep(args.freq)
        rowdict["Abs"] = spec20.reading()
        rowdict["Time"] = (now()-starttime).total_seconds()
        if args.slope is None:
            csvwriter.writerow(rowdict)
        if args.plot or (args.slope is not None):
            timelist.append(rowdict["Time"])
            abslist.append(rowdict["Abs"])
        if rowdict["Time"] > args.time:
            break
    if args.beep is not None:
        spec20.beep(args.beep)
    if args.plot:
        pyplot.plot(timelist, abslist, "ko")
        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Absorbance")
        pyplot.show()
    elif args.slope is not None:
        fitparam = linregress(timelist, abslist)
        rowdict["Slope"] = fitparam[0]
        rowdict["Slope.Err"] = fitparam[4]
        csvwriter.writerow(rowdict)
        slopelist.append(rowdict["Slope"])
        xvarlist.append(float(rowdict[args.slope]))
        pyplot.plot(xvarlist, slopelist, "ko")
        pyplot.xlabel(args.slope)
        pyplot.ylabel("Slope (s^-1)")
        pyplot.show()
    if input("Another reaction? y/n (y) ") not in ["Y", "y", ""]:
        break

# Close the CSV file for good measure
args.file.close()
        
