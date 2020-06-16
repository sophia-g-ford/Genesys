# Overview

The [kinetics.gui](./kinetics.gui) program is designed to collect absorbance
readings at a specified frequency for a specified duration, optionally
analyze the data, and write the data (or analysis) to a CSV file with other
relevant information. The program will also plot data in the CSV file to
enable the user to perform a preliminary viewing of the analysis.

In the graphical user interface, much of the code is involved in structuring
the layout and creating the widgets for the interface. The rest of the
code consists of the callbacks that connect the widgets to the activities
the program performs. This makes the program fairly modular, as opposed
to [enzymekinetics.py](./enzymekinetics.py), which does not rely on many
functions.

To organize the many variables and functions used by the program, the
interface has been arranged in an object-oriented fashion. The main objects
correspond to the three pages in the notebook interface. A fourth object
contains the notebook itself, and serves as the bridge between the other
objects. Most of the attributes and methods of the objects are
self-contained, although there does need to be communication between the
notebooks. The following sections help explain some of the different
methods and attributes used in the interface.

# Spectrometer

The main interactions with the spectrometer are in the Spectrometer tab.
This tab contains widgets for setting data collection parameters important
for adjusting the spectrometer and the data collection using the spectrometer.
The data collected by the spectrometer are stored in attributes of the
object containing the spectrometer tab.

# CSV

The filemanage object contains all the code associated with setting,
creating and adding to the CSV file for storing the data. Because the
format of the CSV file is associated with the type of data that is recorded
by the program (whether raw or analyzed), the object contains code to
read existing CSV files to determine what mode the program runs, and
code to create new CSV files based on the type of mode desired by the
user.

# Analyze

There is an additional tab to plot the processed data contained in the
CSV file. This is currently the least developed of the objects in the
program.
