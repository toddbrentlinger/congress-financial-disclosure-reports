import urllib.request
import xml.etree.ElementTree as ET
# import PyPDF2
import json

from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
# from pdfminer import high_level
# from extract_pdf_tables import extract_pdf_tables_tabula
from os.path import exists

from extract_text import extractTextFromPDF, extractTextFromPDFUsingPDFMiner
from report import Report
from reportlisting import ReportListing

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
        newReportListing = ReportListing(member)
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
        with open('data/report_listings.json', 'r+') as outfile:
            data = [reportListing.convertToJSON() for reportListing in newReportListingsList]
            if outfile.read(2) != '[]':
                data.append(json.load(outfile))
            json.dump(data, outfile, indent=4, ensure_ascii=False)

        # Create reports from new reports list only
        for reportListing in newReportListingsList:
            print(f'Start create report for docID: {reportListing.docID}')
            reportListing.createReport()

        # Add reports from new report listings to JSON file
        with open('data/reports.json', 'r+') as outfile:
            newReportsList = [reportListing.report.convertToJSON() for reportListing in newReportListingsList if reportListing.report]
            if outfile.read(2) != '[]':
                newReportsList.append(json.load(outfile))
            json.dump(newReportsList, outfile, indent=4, ensure_ascii=False)

        # Sort new report listings by filing date (most recent at bottom)
        newReportListingsList.reverse()

    # Print new report listings
    print('\nNew Financial Disclosure Reports:\n')
    for newReport in newReportListingsList:
        print(newReport)
    print('\n')

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
    print(Report(extractTextFromPDF('data/20019331.pdf')))

    # print(extractTextFromPDF('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2015/10013294.pdf'))

    # checkForNewReportListings()

if __name__ == '__main__':
    main()
