import json
from json.decoder import JSONDecodeError

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

    def __init__(self, data, type, bCreateReportNow = False):
        if type == 'xml':
            self.createReportListingFromXML(data, bCreateReportNow)
        elif type == 'json':
            self.createReportListingFromJSON(data, bCreateReportNow)
        else:
            print(f'ERROR: Data type {type} cannot be used to create ReportListing!')

    def __init__old(self, xmlData, bCreateReportNow = False):
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
        
        if bCreateReportNow:
            print(f'Start creating Report from URL: {self.getURL()}')
            self.createReport()
        else:
            self.report = None

        ReportListing.collection.append(self)

    def __eq__(self, other):
        # Check document ID first
        if self.docID != other.docID:
            return False
        # Check if other properties are equal
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

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

        self.report = Report(extractTextFromPDF(self.getURL()), 'string')

    def createReportListingFromXML(self, xmlData, bCreateReportNow = False):
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
        
        if bCreateReportNow:
            print(f'Start creating Report from URL: {self.getURL()}')
            self.createReport()
        else:
            self.report = None

        ReportListing.addToCollection(self)

    def createReportListingFromJSON(self, jsonObj, bCreateReportNow = False):
        self.member = Member(
            prefix=jsonObj['member']['prefix'], 
            firstName=jsonObj['member']['firstName'], 
            lastName=jsonObj['member']['lastName'], 
            suffix=jsonObj['member']['suffix']
        )
        self.filingType = jsonObj['filingType']
        self.stateDistrict = jsonObj['stateDistrict']
        self.year = int(jsonObj['year'])

        dateSplit = jsonObj['filingDate'].split('/')
        self.filingDate = date(int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1]))
        
        self.docID = jsonObj['docID']
        
        if bCreateReportNow:
            self.createReport()
        else:
            self.report = None

        ReportListing.addToCollection(self)

    @classmethod
    def initCollection(cls):
        with open(cls.jsonFile) as outfile:
            try:
                # Get data from JSON file
                data = json.load(outfile)
                for obj in data:
                    # Create class instance for each entry
                    # Append to class collection
                    cls.addToCollection(cls(obj, 'json'))
            except JSONDecodeError: # Error if file is empty
                pass

    @classmethod
    def addToCollection(cls, obj):
        # Check if obj is correct type
        # Check if obj already in collection
        if obj not in cls.collection:
            # Append to collection
            cls.collection.append(obj)