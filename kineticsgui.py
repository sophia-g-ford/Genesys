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
from csv import Sniffer, DictReader, DictWriter
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
writerfields = []
promptentries = {}
promptstrings = {}
promptlabels = {}
def createnewfile(*args):
    additional = additionaltext.get("1.0","end").split(",\n")
    if analysismode.get() == "Time":
        writerfields = ["Reaction"] + additional + ["Time","Abs"]
    elif analysismode.get() == "Slope":
        writerfields = ["Reaction"] + additional + ["Slope","Slope.Err"]
    else:
        # analysismode has not been set to a correct value
        messagebox.showerror(message="Please set mode of recording.")
        return
    with open(csvfile.get(), "w") as fileref:
        csvdict = DictWriter(fileref, fields=writerfields)
        csvdict.write_header()
    reactionnumber.set(0)
    newfile.destroy()
    return
def filenew(*args):
    # New file. Prompt for info from dialog.
    csvfile.set(filedialog.asksaveasfilename())
    newfile = Toplevel()
    newfile.title("New File")
    newframe = ttk.Frame(newfile)
    analysistime = ttk.Radiobutton(newframe, text="Raw",
            variable=analysismode, value="Time")
    analysistime.grid(row=0, column=0)
    analysisslope = ttk.Radiobutton(newframe, text="Linear",
            variable=analysismode, value="Slope")
    analysisslope.grid(row=0, column=1)
    ttk.Label(newframe, text="Additional Columns").grid(row=1,column=0)
#    additionaltext = Text(newframe, width=40, height=10)
#    additionaltext.grid(row=1, column=1)
    cancelnew = ttk.Button(newframe, text="Cancel",
            command=newfile.destroy)
    cancelnew.grid(row=2, column=0)
    savenewbutton = ttk.Button(newframe, text="Create",
            command=createnewfile)
    savenewbutton.grid(row=2, column=1)
    return
def fileselect(*args):
    csvfile.set(filedialog.askopenfilename())
    with open(csvfile.get(), "r") as fileref:
        csvstart = fileref.read(1024)
        if len(csvstart) > 0:
            if not Sniffer().has_header(csvstart):
                messagebox.showinfo(icon="error",
                        message="CSV file contains content but no header!")
                return
            fileref.seek(0)
            csvdict = DictReader(fileref)
            # Determine what mode should be set for data writing
            if "Abs" in csvdict.fieldnames:
                # CSV holds unprocessed data
                writerfields = csvdict.fieldnames
                analysismode.set("Time")
                additional = [field for field in writerfields if field not in ["Reaction","Time","Abs"]]
                for prow, field in enumerate(additional):
                    promptstrings[field] = StringVar()
                    promptlabels[field] = ttk.Label(filemanage, text=field)
                    promptlabels[field].grid(row=3+prow, column=0)
                    promptentries[field] = ttk.Entry(filemanage,
                            textvariable=promptstrings[field])
                    promptentries[field].grid(row=3+prow, column=1)
                for entry in csvdict:
                    reactionnumber.set(entry["Reaction"])
                    for field in additional:
                        promptstrings[field] = entry[field]
            elif "Slope" in csvdict.fieldnames:
                writerfields = csvdict.fieldnames
                analysismode.set("Slope")
                additional = [field for field in writerfields if field != "Reaction"]
                for prow, field in enumerate(additional):
                    promptstrings[field] = StringVar()
                    promptlabels[field] = ttk.Label(filemanage, text=field)
                    promptlabels[field].grid(row=3+prow, column=0)
                    promptentries[field] = ttk.Entry(filemanage,
                            textvariable=promptstrings[field])
                    promptentries[field].grid(row=3+prow, column=1)
                for entry in csvdict:
                    reactionnumber.set(entry["Reaction"])
                    for field in additional:
                        promptstrings[field] = entry[field]
            else:
                # Headers don't correspond to a set generated by this program
                messagebox.showerror(message="CSV file doesn't match those generated by this program.")
        else:
            messagebox.showerror(message="CSV file doesn't contain any content.")
    return

ttk.Label(filemanage, textvariable=csvfile).grid(row=0,column=0,columnspan=2)

filebutton = ttk.Button(filemanage, text="Select...", command=fileselect)
filebutton.grid(row=1,column=0)

newbutton = ttk.Button(filemanage, text="New File", command=filenew)
newbutton.grid(row=1,column=1)

analysismode = StringVar()
reactionnumber = IntVar()

ttk.Label(filemanage, text="Reaction").grid(row=2,column=0)
reactionlabel = ttk.Label(filemanage, textvariable=reactionnumber)
reactionlabel.grid(row=2,column=1)

def writelines(*args):
    messagebox.showinfo(message="This button will trigger writing to the CSV file.")
    return

writebutton = ttk.Button(filemanage, text="Save", command=writelines)
writebutton.grid(row=13,column=0)

ttk.Label(plotting, text="Plot slope as a function of").grid(row=0,column=0)

def plotanalysis(*args):
    messagebox.showinfo(message="The analysis plot should be updated now.")
    return

plotx = StringVar()
plotcombo = ttk.Combobox(plotting, textvariable=plotx)
plotcombo.bind('<<ComboboxSelected>>', plotanalysis)
plotcombo['values'] = ('To', 'Be', 'Computed')
plotcombo.grid(row=0,column=1)

analysisplot = Canvas(plotting)
analysisplot.grid(row=11,column=0,columnspan=2)

root.mainloop()
