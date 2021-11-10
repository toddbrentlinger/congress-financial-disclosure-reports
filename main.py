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

# Extract Text From PDF

# def extractTextFromPDF(filename):
#     extractedText = high_level.extract_text(filename, "", [0])
#     print(extractedText)
#     report = Report(extractedText)
#     print(report)
#     return extractedText

# def extractTextFromPDFOld(filename):
#     # create pdf file object
#     pdfFileObj = open(filename, 'rb')

#     # create a pdf reader object
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#     # Decrypt if needed
#     if pdfReader.isEncrypted:
#         pdfReader.decrypt('')

#     # create a page object
#     pageObj = pdfReader.getPage(0)

#     # extract text from page
#     textData = pageObj.extractText()

#     # close pdf file object
#     pdfFileObj.close()
#     print(textData)
#     return textData

# ---------------------- XML -------------------------------------

# def parseXML(root):
#     reportListingDict = {}
#     for member in root:
#         newReportListing = ReportListing(member)
#         reportListingDict[newReportListing.docID] = newReportListing
#     return reportListingDict

"""Returns non-parsed XML data from zipped XML file."""
def getXMLFromZippedXMLFile(file, bSaveFile = False):
    with ZipFile(file, 'r') as zip:
        zipInfoList = zip.infolist()
        zipInfo = next(filter(lambda zi: zi.filename.endswith('.xml'), zipInfoList), None)
        xmlData = zip.read(zipInfo)
        if bSaveFile:
            zip.extract(zipInfo, 'data')
        zip.close()
        return xmlData

"""Returns parsed XML from url of zipped XML file."""
def getParsedXMLFromURLZippedXMLFile(url, bSaveFile = False):
    remote = urllib.request.urlopen(url) # request remote file
    zippedData = remote.read() # read remote file
    remote.close() # close urllib request

    xmlData = getXMLFromZippedXMLFile(BytesIO(zippedData), bSaveFile)
    return ET.fromstring(xmlData)
    
"""Returns parsed XML from local XML file."""
def getParsedXMLFromXMLFile(filename):
    return ET.parse(filename).getroot()

"""Returns parsed XML using either url of zipped XML file or local XML file."""
def getParsedXMLFromFile(filename):
    return getParsedXMLFromURLZippedXMLFile(filename) if filename.startswith('http') else getParsedXMLFromXMLFile(filename)

# ---------------------- Reports ----------------------------------------

def createReportListingsFromParsedXML(root):
    reportListingDict = {}
    for member in root:
        newReportListing = ReportListing(member)
        reportListingDict[newReportListing.docID] = newReportListing
    return reportListingDict

"""Creates and returns Report from url of zipped XML file or local XML file."""
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
    newReportsDict = createReportListingsFromXMLFile(newReportListingsURL)
    # Check if file exists first. Could be first report listings of new year
    oldReportsDict = createReportListingsFromXMLFile(f'data/{curYear}FD.xml') if exists(f'data/{curYear}FD.xml') else {}

    # Find any new report listings
    newReportsList = []
    for newReportKey in newReportsDict:
        # If newReportKey does NOT exist in OldReportsDict, add to newReportsDict
        if newReportKey not in oldReportsDict:
            newReportsList.append(newReportsDict[newReportKey])

    # If there are new report listings, replace old XML file with new
    if newReportsList:
        getParsedXMLFromURLZippedXMLFile(newReportListingsURL, True)

        # Sort new report listings by filing date (most recent at top)
        newReportsList.sort(key=lambda val: val.filingDate, reverse=True)

        # Add sorted report listings to JSON file
        with open('data/report_listings.json', 'r+') as outfile:
            data = [reportListing.convertToJSON() for reportListing in newReportsList]
            data.append(json.load(outfile))
            json.dump(data, outfile, indent=4, ensure_ascii=False)

        # Add reports from report listings to JSON file
        with open('data/reports.json', 'w+') as outfile:
            reports = json.load(outfile)
            reports.append([(reportListing.report.convertToJSON() if reportListing.report else None) for reportListing in newReportsList])
            json.dump(reports, outfile, indent=4, ensure_ascii=False)

    # Sort new report listings by filing date (most recent at bottom)
    newReportsList.reverse()

    # Print new report listings
    print('New Financial Disclosure Reports')
    for newReport in newReportsList:
        print(newReport)

    return newReportsList

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

    extractTextFromPDF('data/20019530.pdf')
    
    # print(extractTextFromPDF('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2015/10013294.pdf'))

    # checkForNewReportListings()

if __name__ == '__main__':
    main()
