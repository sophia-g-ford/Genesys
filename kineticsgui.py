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

class TestSpec():
    '''This class will serve as a substitute for a spectrometer in
       the absence of an actual Genesys spectrophotometer. The
       class will implement all of the methods of the Genesys
       class, but most will not do anything.'''
    def reading(self):
        return 0.5
    def blank(self):
        return
    def beep(self, times=1):
        messagebox.showinfo(message="The spectrometer should have beeped {} times.".format(times))
        return
    def wavelength(self, wavelength):
        return

class SpecTab():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent.notebook)
        self.parent.notebook.add(self.frame, text="Spectrometer")
        ttk.Label(self.frame, text="Spectrometer").grid(row=0,column=0)
        self.speccombo = ttk.Combobox(self.frame)
        self.speccombo['values'] = ('/dev/usb.serial', '/dev/ttyS0')
        self.speccombo.bind('<<ComboboxSelected>>', self.specselect)
        self.speccombo.grid(row=0,column=1)
        self.wavelength = IntVar()
        ttk.Label(self.frame, text="Wavelength (nm)").grid(row=1,column=0)
        self.waveentry = ttk.Entry(self.frame, textvariable=self.wavelength)
        self.waveentry.grid(row=1,column=1)
        self.frequency = DoubleVar()
        ttk.Label(self.frame, text="Frequency (s)").grid(row=2,column=0)
        self.freqentry = ttk.Entry(self.frame, textvariable=self.frequency)
        self.freqentry.grid(row=2,column=1)
        self.duration = DoubleVar()
        ttk.Label(self.frame, text="Duration (s)").grid(row=3, column=0)
        self.durentry = ttk.Entry(self.frame, textvariable=self.duration)
        self.durentry.grid(row=3,column=1)
        self.blankbutton = ttk.Button(self.frame, text="Blank",
                                      command=self.blank)
        self.blankbutton.grid(row=4,column=0)
        self.runbutton = ttk.Button(self.frame, text="Run",
                                    command=self.collect)
        self.runbutton.grid(row=4,column=1)
        self.runprogress = DoubleVar()
        self.progress = ttk.Progressbar(self.frame, orient=HORIZONTAL,
                mode='determinate', variable=self.runprogress)
        self.progress.grid(row=5,column=0,columnspan=2)
        self.timecourse = Canvas(self.frame)
        self.timecourse.grid(row=6,column=0,columnspan=2)

    def specselect(*args):
        messagebox.showinfo(message="This will be used to select the spectrometer.")
        return

    def blank(*args):
        messagebox.showinfo(message="This will set the wavelength and blank the spectrometer.")
        return

    def collect(*args):
        messagebox.showinfo(message="This will collect data from the spectrometer for the specified period of time.")
        return


class CreateNewFile():
    def __init__(self, parent, filename):
        self.parent = parent
        self.filename = filename
        self.newfile = Toplevel()
        self.newfile.title("New File")
        self.newframe = ttk.Frame(newfile)
        self.newframe.grid()
        self.analysistime = ttk.Radiobutton(self.newframe, text="Raw",
                variable=self.analysismode, value="Time")
        self.analysistime.grid(row=0, column=0)
        self.analysisslope = ttk.Radiobutton(self.newframe, text="Linear",
                variable=self.analysismode, value="Slope")
        self.analysisslope.grid(row=0, column=1)
        ttk.Label(newframe, text="Additional Columns").grid(row=1,column=0)
        self.additionaltext = Text(self.newframe, width=40, height=10)
        self.additionaltext.grid(row=1, column=1)
        self.cancelnew = ttk.Button(self.newframe, text="Cancel",
                command=self.newfile.destroy)
        self.cancelnew.grid(row=2, column=0)
        self.savenewbutton = ttk.Button(self.newframe, text="Create",
                                   command=self.savefile)
        self.savenewbutton.grid(row=2, column=1)
    def savefile(*args):
        additional = self.additionaltext.get("1.0","end").split(",\n")
        if self.analysismode.get() == "Time":
            self.parent.writerfields = ["Reaction"] + additional + ["Time","Abs"]
        elif analysismode.get() == "Slope":
            self.parent.writerfields = ["Reaction"] + additional + ["Slope","Slope.Err"]
        else:
            # analysismode has not been set to a correct value
            messagebox.showerror(message="Please set mode of recording.")
            return
        with open(self.filename, "w") as fileref:
            csvdict = DictWriter(fileref, fields=self.parent.writerfields)
            csvdict.write_header()
        self.parent.reactionnumber.set(0)
        self.parent.csvfile.set(self.filename)
        self.newfile.destroy()
        return

class FileTab():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent.notebook)
        self.parent.notebook.add(self.frame, text="CSV")
        self.csvfile = StringVar()
        self.writerfields = []
        self.promptentries = {}
        self.promptstrings = {}
        self.promptlabels = {}
        ttk.Label(self.frame, textvariable=self.csvfile).grid(row=0,
                                                              column=0,
                                                              columnspan=2)
        self.filebutton = ttk.Button(self.frame, text="Select...",
                                     command=self.fileselect)
        self.filebutton.grid(row=1,column=0)
        self.newbutton = ttk.Button(self.frame, text="New File",
                                    command=self.filenew)
        self.newbutton.grid(row=1,column=1)
        self.analysismode = StringVar()
        self.reactionnumber = IntVar()
        ttk.Label(self.frame, text="Reaction").grid(row=2,column=0)
        self.reactionlabel = ttk.Label(self.frame,
                                       textvariable=self.reactionnumber)
        self.reactionlabel.grid(row=2,column=1)
        self.writebutton = ttk.Button(self.frame, text="Save",
                                      command=self.writelines)
        self.writebutton.grid(row=13,column=0)
    def filenew(*args):
        # New file. Prompt for info from dialog.
        filename = filedialog.asksaveasfilename()
        CreateNewFile(self, filename)
        return
    def fileselect(*args):
        filename = filedialog.askopenfilename()
        with open(filename, "r") as fileref:
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
                    self.csvfile.set(filename)
                    self.writerfields = csvdict.fieldnames
                    self.analysismode.set("Time")
                    additional = [field for field in writerfields if field not in ["Reaction","Time","Abs"]]
                    for prow, field in enumerate(additional):
                        self.promptstrings[field] = StringVar()
                        self.promptlabels[field] = ttk.Label(self.frame,
                                                             text=field)
                        self.promptlabels[field].grid(row=3+prow, column=0)
                        self.promptentries[field] = ttk.Entry(self.frame,
                                textvariable=self.promptstrings[field])
                        self.promptentries[field].grid(row=3+prow, column=1)
                    for entry in csvdict:
                        self.reactionnumber.set(entry["Reaction"])
                        for field in additional:
                            self.promptstrings[field] = entry[field]
                elif "Slope" in csvdict.fieldnames:
                    self.csvfile.set(filename)
                    self.writerfields = csvdict.fieldnames
                    self.analysismode.set("Slope")
                    additional = [field for field in writerfields if field != "Reaction"]
                    for prow, field in enumerate(additional):
                        self.promptstrings[field] = StringVar()
                        self.promptlabels[field] = ttk.Label(self.frame,
                                                             text=field)
                        self.promptlabels[field].grid(row=3+prow, column=0)
                        self.promptentries[field] = ttk.Entry(self.frame,
                                textvariable=self.promptstrings[field])
                        self.promptentries[field].grid(row=3+prow, column=1)
                    for entry in csvdict:
                        self.reactionnumber.set(entry["Reaction"])
                        for field in additional:
                            self.promptstrings[field] = entry[field]
                else:
                    # Headers don't correspond to a set generated by this program
                    messagebox.showerror(message="CSV file doesn't match those generated by this program.")
            else:
                messagebox.showerror(message="CSV file doesn't contain any content.")
        return

    def writelines(*args):
        messagebox.showinfo(message="This button will trigger writing to the CSV file.")
        return

class PlotTab():
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent.notebook)
        self.parent.notebook.add(self.frame, text="Plot")
        ttk.Label(self.frame, text="Plot slope as a function of").grid(row=0,
                                                                       column=0)
        self.plotx = StringVar()
        self.plotcombo = ttk.Combobox(self.frame, textvariable=self.plotx)
        self.plotcombo.bind('<<ComboboxSelected>>', self.plotanalysis)
        self.plotcombo['values'] = ('To', 'Be', 'Computed')
        self.plotcombo.grid(row=0,column=1)
        self.analysisplot = Canvas(self.frame)
        self.analysisplot.grid(row=11,column=0,columnspan=2)

    def plotanalysis(*args):
        messagebox.showinfo(message="The analysis plot should be updated now.")
        return

class KineticsGUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Absorbance Kinetics")
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0)
        self.operation = SpecTab(self)
        self.filemanage = FileTab(self)
        self.plotting = PlotTab(self)
        
root = Tk()
KineticsGUI(root)
root.mainloop()
