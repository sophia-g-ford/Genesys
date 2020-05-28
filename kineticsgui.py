# This program will create a user interface for interacting with
# the Genesys class for collecting time-dependent data.
#
# The initial design for the interface will be a notebook
# interface, with one tab for spectrometer operation, one
# for data saving, and one for plotting analyzed data.

# This program will require the Tk widgets, particularly
# the themed widgets, the Genesys class from this module,
# the Scipy module for fitting the data, the csv module
# for reading and writing the data to CSV files, and the
# matplotlib package for plotting the data.
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
# from genesys import Genesys
# from datetime import datetime
# from time import sleep
# from csv import Sniffer, DictReader, DictWriter
# from scipy.stats import linregress
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

root = Tk()
root.title("Absorbance Kinetics")

notebook = ttk.Notebook(root)
operation = ttk.Frame(notebook)
filemanage = ttk.Frame(notebook)
plotting = ttk.Frame(notebook)
notebook.add(operation, text="Spectrometer")
notebook.add(filemanage, text="CSV")
notebook.add(plotting, text="Plot")
notebook.grid(row=0, column=0)

def specselect(*args):
    messagebox.showinfo(message="This will be used to select the spectrometer.")
    return

ttk.Label(operation, text="Spectrometer").grid(row=0,column=0)
speccombo = ttk.Combobox(operation)
speccombo['values'] = ('/dev/usb.serial', '/dev/ttyS0')
speccombo.bind('<<ComboboxSelected>>', specselect)
speccombo.grid(row=0,column=1)

wavelength = StringVar()
ttk.Label(operation, text="Wavelength (nm)").grid(row=1,column=0)
waveentry = ttk.Entry(operation, textvariable=wavelength)
waveentry.grid(row=1,column=1)

frequency = StringVar()
ttk.Label(operation, text="Frequency (s)").grid(row=2,column=0)
freqentry = ttk.Entry(operation, textvariable=frequency)
freqentry.grid(row=2,column=1)

duration = StringVar()
ttk.Label(operation, text="Duration (s)").grid(row=3, column=0)
durentry = ttk.Entry(operation, textvariable=duration)
durentry.grid(row=3,column=1)

def blank(*args):
    messagebox.showinfo(message="This will set the wavelength and blank the spectrometer.")
    return

blankbutton = ttk.Button(operation, text="Blank", command=blank)
blankbutton.grid(row=4,column=0)

def collect(*args):
    messagebox.showinfo(message="This will collect data from the spectrometer for the specified period of time.")
    return

runbutton = ttk.Button(operation, text="Run", command=collect)
runbutton.grid(row=4,column=1)

runprogress = DoubleVar()
progress = ttk.Progressbar(operation, orient=HORIZONTAL,
        mode='determinate', variable=runprogress)
progress.grid(row=5,column=0,columnspan=2)

timecourse = Canvas(operation)
timecourse.grid(row=6,column=0,columnspan=2)

csvfile = StringVar()
def fileselect(*args):
    csvfile.set(filedialog.askopenfilename())
    return

filebutton = ttk.Button(filemanage, text="Select...", command=fileselect)
filebutton.grid(row=0,column=0)

ttk.Label(filemanage, textvariable=csvfile).grid(row=0,column=1)

analysistype = StringVar()

def writelines(*args):
    messagebox.showinfo("This button will trigger writing to the CSV file.")
    return

writebutton = ttk.Button(filemanage, text="Save", command=writelines)
writebutton.grid(row=11,column=0)

ttk.Label(plotting, text="Plot {0} as a function of".format(analysistype)).grid(row=0,column=0)

def plotanalysis(*args):
    messagebox.showinfo("The analysis plot should be updated now.")
    return

plotx = StringVar()
plotcombo = ttk.Combobox(plotting, textvariable=plotx)
plotcombo.bind('<<ComboboxSelected>>', plotanalysis)
plotcombo['values'] = ('To', 'Be', 'Computed')
plotcombo.grid(row=0,column=1)

analysisplot = Canvas(plotting)
analysisplot.grid(row=11,column=0,columnspan=2)

root.mainloop()
