from tkinter import *
from tkinter import ttk

from verticalscrolledframe import VerticalScrolledFrame
from displaylist import ReportListingsFrame

# Import From Parent Directory
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current))
from main import checkForNewReportListings
from reportlisting import ReportListing
from report import Report
from transaction import Transaction

class CongressFinancialDisclosureReportsApp(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)

        root.title('U.S Congress Financial Disclosure Reports')

        # Styles
        s = ttk.Style()
        s.configure('TopBarBtn.TButton', foreground='grey', background='white')
        s.configure('TopBarBtnActive.TButton', foreground='white', background='grey')

        # Main Frame needed to use newer "themed" widgets
        mainframe = ttk.Frame(root, padding='5')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ReportListingsFrame(root).grid()

def main():
    ReportListing.initCollection()
    Report.initCollection()

    # root = Tk()
    # ReportListingsFrame(root).grid()
    # root.mainloop()

    root = Tk()
    CongressFinancialDisclosureReportsApp(root).grid()
    root.mainloop()

if __name__ == '__main__':
    main()