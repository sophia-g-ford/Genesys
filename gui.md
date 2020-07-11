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

## changewavelength

This callback that is used when the wavelength changes needs some
explanation. The callback is executed when the user changes the value in
the wavelength entry box. Unfortunately, it executes this call back with
every change, including clearing the box and typing every digit of the
wavelength. Since the program should adjust the wavelength setting only
when a valid wavelength is entered, the callback checks the value in the
variable to see if it's large enough to be the wavelength of a visible
spectrometer. The code is wrapped in a try/except structure to catch the
exception that occurs when the box is empty.

## collect

The callback responding to the Collect button is divided up into two methods.
The first sets initial parameters for the data collection, like setting
empty lists for times and absorbance, and determining the starting time of
the reaction. The starting time is then passed to another method that adds
data to the times and absorbance lists, calling itself recursively until
the duration of the reaction has been passed. This division of labor into
two methods allows the second method to be called using the *after* method
of Tk widgets, to take advantage of the threading inherent in GUI interfaces.
The main purpose of using the threading is so that the progress bar updates
appropriately. The *after* method requires as its first argument the number
of milliseconds to wait before executing the function specified. This
number of milliseconds must be an integer, which is why the first argument
to the method is specified the way it is.

# CSV

The filemanage object contains all the code associated with setting,
creating and adding to the CSV file for storing the data. Because the
format of the CSV file is associated with the type of data that is recorded
by the program (whether raw or analyzed), the object contains code to
read existing CSV files to determine what mode the program runs, and
code to create new CSV files based on the type of mode desired by the
user.

## Variables

The FileTab object keeps track of the name of the CSV file in the
variable csvfile. It keeps track of the reaction number in
reactionnumber. It has a list called writerfields that keeps track of
the headers to be used in the CSV file. It also contains attributes
called promptentries, promptstrings and promptlabels, which are
dictionaries for the Entry widgets, StringVar objects and Label widgets,
respectively, for the values in the CSV file that must be supplied by the
user, rather than measured by the program. The object contains an
analysismode attribute that determines what type of data is written to
the CSV file. Currently, the only values that analysismode can take are
"Time", where the absorbance is recorded as a function of time, and "Slope",
where the slope of the best-fit line to the absorbance as a function of
time is recorded.

## filenew

The filenew method of the FileTab object mainly creates a new window called
CreateNewFile. This window has widgets to select the type of analysis
to be performed on the data, as well as a text box to list the columns
to be written to the file that will contain information supplied by the
user. When the file is created (using the savefile method of the
CreateNewFile object), the column names supplied by the user and the
column names appropriate to the analysis type are written to the file
named according to the filename specified in the dialog immediately
preceding the creation of the CreateNewFile object.

# Analyze

There is an additional tab to plot the processed data contained in the
CSV file. This is currently the least developed of the objects in the
program.
