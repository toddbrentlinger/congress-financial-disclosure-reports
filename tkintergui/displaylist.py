from tkinter import ttk
from tkinter.constants import N, W, E, S

# Import from parent directory
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current))
# Modules imported from parent directory
from main import checkForNewReportListings
from reportlisting import ReportListing
from report import Report
from transaction import Transaction

class DisplayListBaseFrame(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # Main Frame Column Configure
        parent.columnconfigure(0, minsize=100, weight=1)
        parent.columnconfigure(1, minsize=350, weight=1)
        parent.columnconfigure(2, minsize=50, weight=1)

        # Main Frame Row Configure
        parent.rowconfigure(0, minsize=50, weight=1)
        parent.rowconfigure(1, minsize=400, weight=1)
        parent.rowconfigure(2, minsize=50, weight=1)
        
        # Top Bar
        topBarFrame = ttk.Frame(parent, borderwidth=2, relief='groove')
        topBarFrame.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))

        # Top Bar Row/Column Configure
        for i in range(3):
            topBarFrame.columnconfigure(i, weight=1)
        topBarFrame.rowconfigure(0, weight=1)

        # Display Buttons/Tabs - Active Tab is highlighted
        self.topBarBtns = {}
        self.topBarBtns['reportListings'] = ttk.Button(topBarFrame, text='Report Listings', style='TopBarBtnActive.TButton', command=self.handleDisplayReportListingsBtnClick)
        self.topBarBtns['reports'] = ttk.Button(topBarFrame, text='Reports', style='TopBarBtn.TButton', command=self.handleDisplayReportsBtnClick)
        self.topBarBtns['transactions'] = ttk.Button(topBarFrame, text='Transactions', style='TopBarBtn.TButton', command=self.handleDisplayTransactionsBtnClick)
        for index, btn in enumerate(self.topBarBtns.values()):
            btn.grid(column=index, row=0, sticky=(N, W, E, S))

        # Left Side Bar - Filter options for each tab
        self.leftSideBarFrame = ttk.Frame(parent, borderwidth=2, relief='groove')
        self.leftSideBarFrame.grid(column=0, row=1, sticky=(N, W, E, S))

        # Left Side Bar Row/Column Configure
        self.leftSideBarFrame.columnconfigure(0, weight=1)
        self.leftSideBarFrame.rowconfigure(0, weight=1)

        # Content
        self.contentFrame = ttk.Frame(parent, borderwidth=2, relief='groove')
        self.contentFrame.grid(column=1, row=1, sticky=(N, W, E, S))
        self.contentFrame.columnconfigure(0, weight=1)
        self.contentFrame.rowconfigure(0, weight=1)
        self.contentFrame.rowconfigure(1, weight=1)
        self.contentFrame.rowconfigure(2, weight=1)

        # Content - Top
        self.contentTopBarFrame = ttk.Frame(self.contentFrame, borderwidth=2, relief='groove')
        self.contentTopBarFrame.grid(column=0, row=0)
        # Content - Main
        self.contentMainFrame = ttk.Frame(self.contentFrame, borderwidth=2, relief='groove')
        self.contentMainFrame.grid(column=0, row=1, sticky=(N, W, E, S))
        # Content - Bottom
        self.contentBottomBarFrame = ttk.Frame(self.contentFrame, borderwidth=2, relief='groove')
        self.contentBottomBarFrame.grid(column=0, row=2)

        # Right Side Bar
        self.rightSideBarFrame = ttk.Frame(parent, borderwidth=2, relief='groove')
        self.rightSideBarFrame.grid(column=2, row=1, sticky=(N, W, E, S))

        # Ride Side Bar Row/Column Configure
        self.rightSideBarFrame.columnconfigure(0, weight=1)
        self.rightSideBarFrame.rowconfigure(0, weight=1)

        checkNewReportsBtn = ttk.Button(self.rightSideBarFrame, text='Update Reports', command=self.handleCheckForNewReportsClick)
        checkNewReportsBtn.grid(column=0, row=0, sticky=(W, E, S))
        
        # Footer
        self.footerFrame = ttk.Frame(parent, borderwidth=2, relief='groove')
        self.footerFrame.grid(column=0, row=2, columnspan=3, sticky=(N, W, E, S))

    def handleCheckForNewReportsClick(self):
        checkForNewReportListings()
        # self.displayReportListings()

    def handleDisplayReportListingsBtnClick(self):
        pass

    def handleDisplayReportsBtnClick(self):
        pass

    def handleDisplayTransactionsBtnClick(self):
        pass

class ReportListingsFrame(DisplayListBaseFrame):
    def __init__(self, parent, *args, **kwargs):
        DisplayListBaseFrame.__init__(self, parent, *args, **kwargs)

        self.updateReportListings()

    def updateReportListings(self):
        self.contentMainFrame.columnconfigure(0, weight=1)
        self.contentMainFrame.rowconfigure(0, weight=1)

        listFrame = ttk.Frame(self.contentMainFrame)
        listFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        listFrame.columnconfigure(0, weight=1)
        for i in range(5):
            listFrame.rowconfigure(i, weight=1)

        # Add filter options to left side bar frame

        # Add report listings to content frame
        for index, reportListing in enumerate(ReportListing.collection):
            if index >= 5:
                break

            reportListingFrame = ttk.Frame(listFrame, borderwidth=2, relief='groove')
            reportListingFrame.grid(column=0, row=index, sticky=(N, W, E, S))
            for i in range(2):
                reportListingFrame.columnconfigure(i, weight=1)

            # Add Member name
            ttk.Label(reportListingFrame, text='Member: ').grid(column=0, row=0, sticky=(N, W, E, S))
            ttk.Label(reportListingFrame, text=reportListing.member).grid(column=1, row=0, sticky=(N, W, E, S))
            # Add Doc ID
            ttk.Label(reportListingFrame, text='Doc ID: ').grid(column=0, row=1, sticky=(N, W, E, S))
            ttk.Label(reportListingFrame, text=reportListing.docID).grid(column=1, row=1, sticky=(N, W, E, S)) 

    def handleCheckForNewReportsClick(self):
        DisplayListBaseFrame.handleCheckForNewReportsClick(self)
        self.updateReportListings()
