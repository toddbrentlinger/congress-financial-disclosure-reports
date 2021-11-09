import urllib.request
import xml.etree.ElementTree as ET
import PyPDF2

from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from pdfminer import high_level
from extract_pdf_tables import extract_pdf_tables_tabula
from report import Report
from reportlisting import ReportListing

# Extract Text From PDF

def extractTextFromPDF(filename):
    extractedText = high_level.extract_text(filename, "", [0])
    # print(extractedText)
    report = Report(extractedText)
    print(report)
    return extractedText

def extractTextFromPDFOld(filename):
    # create pdf file object
    pdfFileObj = open(filename, 'rb')

    # create a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Decrypt if needed
    if pdfReader.isEncrypted:
        pdfReader.decrypt('')

    # create a page object
    pageObj = pdfReader.getPage(0)

    # extract text from page
    textData = pageObj.extractText()

    # close pdf file object
    pdfFileObj.close()
    print(textData)
    return textData

# XML

def parseXML(root):
    reportListingDict = {}
    for member in root:
        newReportListing = ReportListing(member)
        reportListingDict[newReportListing.docID] = newReportListing
    return reportListingDict

def getXMLFromZipFile(file, bSaveFile = False):
    with ZipFile(file, 'r') as zip:
        zipInfoList = zip.infolist()
        zipInfo = next(filter(lambda zi: zi.filename.endswith('.xml'), zipInfoList), None)
        xmlData = zip.read(zipInfo)
        if bSaveFile:
            zip.extract(zipInfo, 'data')
        zip.close()
        return xmlData

def getXMLFromURL(url):
    remote = urllib.request.urlopen(url) # request remote file
    zippedData = remote.read() # read remote file
    remote.close() # close urllib request

    xmlData = getXMLFromZipFile(BytesIO(zippedData))
    return ET.fromstring(xmlData)
    
def getXMLFromFile(filename):
    return ET.parse(filename).getroot()

# Reports

def getReport(filename):
    xmlData = getXMLFromURL(filename) if filename.startswith('http') else getXMLFromFile(filename)
    return parseXML(xmlData)

def downloadReports():
    for year in range(2008, datetime.today().year + 1):
        getReport(f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{str(year)}FD.ZIP')

def compareReports(newReportsFilename, oldReportsFilename):
    newReportsDict = getReport(newReportsFilename)
    oldReportsDict = getReport(oldReportsFilename)

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

# Main

def main():
    # downloadReports()
    # getReport('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP')

    # compareReports('https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP', 'data/2021FD.xml')

    extractTextFromPDF('data/20019331.pdf')
    extractTextFromPDF('data/20019771.pdf')

    # extract_pdf_tables_tabula('20019331.pdf')

if __name__ == '__main__':
    main()
