from datetime import datetime, date

from extract_text import extractTextFromPDF
from report import Report

class Member:
    # members = []

    def __init__(self, **kwargs):
        self.prefix = kwargs['prefix']
        self.lastName = kwargs['lastName']
        self.firstName = kwargs['firstName']
        self.suffix = kwargs['suffix']

        # Member.members.append(self)

    def __str__(self):
        return f'{self.prefix + " " if self.prefix else ""}{self.firstName} {self.lastName}{" " + self.suffix if self.suffix else ""}'

    def convertToJSON(self):
        return {
            'prefix': self.prefix,
            'lastName': self.lastName,
            'firstName': self.firstName,
            'suffix': self.suffix
        }

class ReportListing:
    collection = []
    jsonFile = 'data/report_listings.json'

    def __init__(self, xmlData):
        self.member = Member(prefix=xmlData[0].text, lastName=xmlData[1].text, firstName=xmlData[2].text, suffix=xmlData[3].text)

        self.filingType = xmlData[4].text
        self.stateDistrict = xmlData[5].text
        self.year = int(xmlData[6].text)

        if xmlData[7].text:
            filingDateSplit = xmlData[7].text.split('/')
            self.filingDate = date(int(filingDateSplit[2]), int(filingDateSplit[0]), int(filingDateSplit[1]))
        else:
            self.filingDate = date.today()
        
        self.docID = xmlData[8].text

        print(f'Report Listing URL: {self.getURL()} finished!')
        self.report = self.createReport()
        # self.report = None
        ReportListing.collection.append(self)

    def __str__(self):
        return f'{self.member} - FilingDate: {self.filingDate} - ReportURL: {self.getURL()}'

    def convertToJSON(self):
        return {
            'member': self.member.convertToJSON(),
            'filingType': self.filingType,
            'stateDistrict': self.stateDistrict,
            'year': self.year,
            'filingDate': self.filingDate.strftime('%m/%d/%Y'),
            'docID': self.docID,
            'report': self.report.convertToJSON() if self.report else None,
        }

    def getURL(self):
        # If docID begins with 2, use:
        # https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{self.year}/{self.docID}.pdf
        # Else use:
        # https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{self.year}/{self.docID}.pdf
        if self.docID.startswith('2'):
            return f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{str(self.year)}/{self.docID}.pdf'
        else:
            return f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{str(self.year)}/{self.docID}.pdf'

    def createReport(self):
        # Check docID
        if not self.docID.startswith('200'):
            return None

        return Report(extractTextFromPDF(self.getURL()))
