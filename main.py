import urllib.request
import xml.etree.ElementTree as ET
# import PyPDF2
import json
import time
from json.decoder import JSONDecodeError

from datetime import datetime, date, timedelta
from zipfile import ZipFile
from io import BytesIO
# from pdfminer import high_level
# from extract_pdf_tables import extract_pdf_tables_tabula
from os.path import exists

from extract_text import extractTextFromPDF, extractTextFromPDFUsingPDFMiner
from report import Report
from reportlisting import ReportListing
from twiliosms.main import sendTextMessage

"""Returns file object of zip file from url."""
def getZipFileFromURL(url):
    remote = urllib.request.urlopen(url) # request remote file
    zippedData = remote.read() # read remote file
    remote.close() # close urllib request
    return BytesIO(zippedData)

# ---------------------- XML -------------------------------------

"""Returns non-parsed XML data from zipped XML file."""
def getXMLFromZipFile(file, bSaveFile = False):
    with ZipFile(file, 'r') as zip:
        zipInfoList = zip.infolist()
        xmlFile = next(filter(lambda zi: zi.filename.endswith('.xml'), zipInfoList), None)
        xmlData = zip.read(xmlFile)
        if bSaveFile:
            zip.extract(xmlFile, 'data')
        zip.close()
        return xmlData

"""Returns parsed XML from url of zip file containing XML file."""
def getParsedXMLFromURLZipFile(url, bSaveFile = False):
    xmlData = getXMLFromZipFile(getZipFileFromURL(url), bSaveFile)
    return ET.fromstring(xmlData)

"""Returns parsed XML from local XML file."""
def getParsedXMLFromXMLFile(filename):
    return ET.parse(filename).getroot()

"""Returns parsed XML using either url of zip file containing XML file or local XML file."""
def getParsedXMLFromFile(filename):
    return getParsedXMLFromURLZipFile(filename) if filename.startswith('http') else getParsedXMLFromXMLFile(filename)

# ---------------------- Reports ----------------------------------------

def createReportListingsFromParsedXML(root):
    reportListingDict = {}
    nMembers = len(root)
    count = 1
    print('\nStarting to create report listings.')
    for member in root:
        newReportListing = ReportListing(member, 'xml')
        reportListingDict[newReportListing.docID] = newReportListing
        print(f'Report Listing Finished: {count} / {nMembers}', end='\r', flush=True)
        count += 1
    print(f'Finished creating {nMembers} report listings!')
    return reportListingDict

"""Creates and returns Report from url of zipfile containg XML file or local XML file."""
def createReportListingsFromXMLFile(filename):
    return createReportListingsFromParsedXML(getParsedXMLFromFile(filename))

def downloadReports():
    for year in range(2008, datetime.today().year + 1):
        createReportListingsFromXMLFile(f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{str(year)}FD.ZIP')

def compareReports(newReportsFilename, oldReportsFilename):
    newReportsDict = createReportListingsFromXMLFile(newReportsFilename)
    oldReportsDict = createReportListingsFromXMLFile(oldReportsFilename)

    newReportsList = []
    for newReportKey in newReportsDict:
        # If newReportKey does NOT exist in OldReportsDict, add to newReportsDict
        if newReportKey not in oldReportsDict:
            newReportsList.append(newReportsDict[newReportKey])

    # If there are new reports, replace old file with new file
    if newReportsList:
        pass

    def sortByFilingDate(val):
        return val.filingDate
    newReportsList.sort(key=sortByFilingDate)

    print('New Financial Disclosure Reports')
    for newReport in newReportsList:
        print(newReport)

"""Compare newest zip file on site with equivalent current XML file saved to record"""
def checkForNewReportListings():
    curYear = str(datetime.now().year)
    newReportListingsURL = f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{curYear}FD.ZIP'

    newReportListingsDict = createReportListingsFromXMLFile(newReportListingsURL)
    # Check if file exists first. Could be first report listings of new year.
    oldReportListingsDict = createReportListingsFromXMLFile(f'data/{curYear}FD.xml') if exists(f'data/{curYear}FD.xml') else {}

    # Find any new report listings
    newReportListingsList = []
    for key, value in newReportListingsDict.items():
        # If key does NOT exist in oldReportListingsDict, add to newReportListingsList
        if key not in oldReportListingsDict:
            newReportListingsList.append(value)

    # If there are new report listings
    if newReportListingsList:
        print(f'\nThere are {len(newReportListingsList)} new Reports!\n')

        # Replace old XML file with new
        # TODO: Creates another request for pdf and unzips to get xml. Can save file object of XML file from zip file.
        getParsedXMLFromURLZipFile(newReportListingsURL, True)

        # Sort new report listings by filing date (most recent at top)
        newReportListingsList.sort(key=lambda val: val.filingDate, reverse=True)

        # Add sorted new report listings to JSON file
        data = [reportListing.convertToJSON() for reportListing in newReportListingsList]
        with open('data/report_listings.json') as outfile:
            try:
                data.extend(json.load(outfile))
            except JSONDecodeError: # Error if file is empty
                pass
        with open('data/report_listings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        # Create reports from new reports list only
        for reportListing in newReportListingsList:
            print(f'Start create report for docID: {reportListing.docID}')
            reportListing.createReport()

        # Add reports from new report listings to JSON file
        data = [reportListing.report.convertToJSON() for reportListing in newReportListingsList if reportListing.report]
        with open('data/reports.json') as outfile:
            try:
                data.extend(json.load(outfile))
            except JSONDecodeError: # Error if file is empty
                pass
        with open('data/reports.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        # Sort new report listings by filing date (most recent at bottom)
        newReportListingsList.reverse()

        # Print new report listings
        print('\nNew Financial Disclosure Reports:\n')
        for newReport in newReportListingsList:
            print(newReport)
        print('\n')
    else:
        print('\nNo New Financial Disclosure Reports\n')

    return newReportListingsList

# Main

def main():
    # downloadReports()
    # createReportListingsFromXMLFile('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP')

    # compareReports('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP', 'data/2021FD.xml')

    # extract_pdf_tables_tabula('20019331.pdf')

    # print(Report(extractTextFromPDF('data/20019331.pdf')))
    # print(Report(extractTextFromPDF('data/20019771.pdf')))
    # print(Report(extractTextFromPDF('data/20019530.pdf')))
    # print(Report(extractTextFromPDF('data/20017909.pdf')))

    # extractTextFromPDF('data/20019530.pdf')
    # print(Report(extractTextFromPDF('data/20019331.pdf')))

    # print(extractTextFromPDF('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2015/10013294.pdf'))
    # print(extractTextFromPDF('https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/20019922.pdf'))

    ReportListing.initCollection()
    Report.initCollection()
    # checkForNewReportListings()

    count = 0
    while True or count < 5:
        newReportListings = checkForNewReportListings()

        # Text any stock transactions from newReportListings
        # textMessageList = [] # Each element is within Twilio character limit for text messaging (1900)
        # textMessage = ""
        stockTransactions = []
        for reportListing in newReportListings:
            if not reportListing.report:
                continue

            for transaction in reportListing.report.transactions:
                if transaction.asset.typeCode == 'ST':
                    # stockTransactions.append(transaction)
                    stockTransactions.append(
                        (reportListing.member, transaction),
                    )

            # if stockTransactions:
            #     textMessage += f"\n{reportListing.member}\n"
            #     currDate = date.today()
            #     for stockTransaction in stockTransactions:
            #         if stockTransaction.filingDate != currDate:
            #             currDate = stockTransaction.filingDate
            #             textMessage += f'\n{currDate.strftime("%m/%d/%Y")}\n'
            #         textMessage += f'\n{stockTransaction.asset.title} [{stockTransaction.type}]\n{stockTransaction.amount}\n'

        # if textMessage:
        #     # Send text message using Twilio
        #     #sendTextMessage(textMessage)
        #     print(f'Text Message ({len(textMessage)} chars): \n', textMessage)

        if stockTransactions:
            # Sort stock transactions by date (newest to oldest)
            stockTransactions.sort(key=lambda transaction: transaction[1].filingDate)
            stockTransactions.reverse()

            # Remove stock transactions older 30 days
            dateLimit = date.today() - timedelta(days=30)
            stockTransactions = filter(lambda transaction: transaction[1].filingDate > dateLimit, stockTransactions)

            # Create array of strings with each index holding all stock transactions for one date
            transactionStrList = []
            tempDate = None
            tempStr = ''
            for stockTransaction in stockTransactions:
                if stockTransaction[1].filingDate != tempDate:
                    # Add tempStr to transactionStrList and reset it's value to empty string
                    if tempStr:
                        transactionStrList.append(tempStr)
                        tempStr = ''
                    tempDate = stockTransaction[1].filingDate
                    tempStr += f'\n{tempDate.strftime("%m/%d/%Y")}\n'
                tempStr += f'\n{stockTransaction[1].asset.title} [{stockTransaction[1].type}]\n{stockTransaction[1].amount}\n{stockTransaction[0]}\n'

            # Send text message with Twilio (limited to 1600 characters per text message)
            print(transactionStrList)

        # Sleep for 15 minutes before starting loop over
        count += 1
        time.sleep(900)

if __name__ == '__main__':
    main()
