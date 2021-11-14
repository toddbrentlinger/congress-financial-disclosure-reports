from tkinter import *
from tkinter import ttk

from main import checkForNewReportListings

def handleCheckForNewReportsClick():
    checkForNewReportListings()

def createCustomWindow():
    root = Tk()

    # Top Bar

    # Left Side Bar

    # Main

    # Right Side Bar

    # Footer

    root.mainloop()

def main():
    root = Tk()
    root.title('U.S Congress Financial Disclosure Reports')

    # Main Frame needed to use newer "themed" widgets
    mainframe = ttk.Frame(root, padding='5')
    mainframe.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Top Bar
    topBarFrame = ttk.Frame(mainframe, borderwidth=2, relief='groove')
    topBarFrame.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))
    mainframe.rowconfigure(0, minsize=20, weight=1)

    # Side Bar
    sideBarFrame = ttk.Frame(mainframe, borderwidth=2, relief='groove')
    sideBarFrame.grid(column=0, row=1, sticky=(N, W, E, S))
    mainframe.rowconfigure(1, minsize=100, weight=5)
    mainframe.columnconfigure(0, minsize=50, weight=5)

    checkNewReportsBtn = ttk.Button(sideBarFrame, text='Check For New Reports', command=handleCheckForNewReportsClick)

    # Display Data
    displayFrame = ttk.Frame(mainframe, borderwidth=2, relief='groove')
    displayFrame.grid(column=1, row=1, sticky=(N, W, E, S))
    mainframe.columnconfigure(1, minsize=100, weight=10)
    
    root.mainloop()

if __name__ == '__main__':
    main()