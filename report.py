from json.decoder import JSONDecodeError
import re
import statistics
import json

from datetime import datetime
from transaction import Transaction

class Report:
    collection = []
    jsonFile = 'data/reports.json'

    def __init__(self, data, type, year = datetime.now().year):
        if type == 'string':
            self.createReportFromString(data, year)
        elif type == 'json':
            self.createReportFromJSON(data)
        else:
            print(f'ERROR: Data type {type} cannot be used to create Report!')
            return
        self.year = year

    def __init__old(self, extractedText, year = datetime.now().year):
        self.messageFlags = []
        self.year = year

        self.docID = re.search('(?<=Filing ID #)\d+', extractedText, re.IGNORECASE).group()
        self.name = re.search('(?<=Status:)(?:\\n)+([\w. ]+)', extractedText).group(1)
        self.stateDistrict = re.search('(?<=State\/District:\s)[\d\w]+', extractedText).group()

        # Transactions
        data = {}

        data['assetTitleList'] = []
        # Replace every single instance of \n (NOT \n\n) with single space. Helps with regex.
        regExp = re.compile('(?<!(?:\\n))(?:\\n)(?!(?:\\n))')
        extractedTextModified = regExp.sub(' ', extractedText)
        # Find every text between \n\n and \n\n
        matchList = re.findall('(?<=(?:\\n){2}).+?(?=(?:\\n){2})', extractedTextModified)
        for match in matchList:
            # If str ends with '[NN]', where N is any uppercase letter, add rest of string to asset title list
            searchMatch = re.search('.+?(?=(?:\\n)|\s\[[A-Z]{2}\])', match)
            if searchMatch is not None:
                data['assetTitleList'].append(searchMatch.group())

        # Use non-modified extracted text. Could change in future to only use matchList

        data['ownerList'] = re.findall('(?<=(?:\\n){2})[A-Z]{2}(?=(?:\\n){2})', extractedText) # Full match, no capture group
        # Remove any matches of 'ID'
        data['ownerList'] = [ owner for owner in data['ownerList'] if owner != 'ID' ]

        data['assetTypeCodeList'] = re.findall('(?<=\[)[a-zA-Z]+?(?=(?=\]\\n){2}|\]\s)', extractedText) # Full match, no capture group
        # Convert to uppercase (case where letter is parsed as lower but should be upper)
        data['assetTypeCodeList'] = [ typeCode.upper() for typeCode in data['assetTypeCodeList'] ]

        # Asset should include either a description or subholding of. Have only seen reports with one or the other.
        data['assetDescriptionList'] = re.findall('(?<=description:\s).+?(?=(?:\\n){2})', extractedText, re.IGNORECASE) # Full match, no capture group
        data['assetSubholdingOf'] = re.findall('(?<=subholding\sof:\s).+?(?=(?:\\n){2})', extractedText, re.IGNORECASE)

        data['assetFilingStatusList'] = re.findall('(?<=filing\sstatus: ).+?(?=(?:\\n))', extractedText, re.IGNORECASE) # Full match, no capture group
        data['transactionTypeList'] = re.findall('(?<=(?:\\n){2}|\] )[A-Z](?: \(partial\))?(?=(?:\\n){2})', extractedText) # Full match, no capture groups
        data['datesList'] = re.findall('(?<=(?:\\n){2})([\d\/]+)\s([\d\/]+)(?=(?:\\n){2})', extractedText) # Two capture groups
        data['amountList'] = re.findall('\$[\d,]+?\s-(?:\\n)*\s*\$[\d,]+?(?=(?:\\n){2})', extractedText) # Full match, no capture group

        # Check for missing values that weren't captured

        nTransactions = statistics.mode([len(data[key]) for key in data])

        # Do NOT check owner list (most often left blank)
        # Do NOT check description or subholdingOf (could have one, both, or none)
        keysToSkip = ['ownerList', 'assetDescriptionList', 'assetSubholdingOf']
        
        for key, list in data.items():
            if len(list) < nTransactions:
                if key not in keysToSkip:
                    # Add message flag
                    self.messageFlags.append(f'{key} has missing values!')
                    print(f'{key} has missing values!')
                # Change list length to match nTransactions using empty string as value
                list.extend(['' for i in range(nTransactions - len(list))])
            elif len(list) > nTransactions:
                if key not in keysToSkip:
                    # Add message flag
                    self.messageFlags.append(f'{key} has too many values!')
                    print(f'{key} has too many values!')

        self.transactions = []
        for i in range(nTransactions):
            newTransaction = Transaction(
                owner=data['ownerList'][i].replace('\n', ' '),
                asset={
                    'title': data['assetTitleList'][i].replace('\n', ' '), 
                    'typeCode': data['assetTypeCodeList'][i].replace('\n', ' '), 
                    'filingStatus': data['assetFilingStatusList'][i].replace('\n', ' '), 
                    'description': data['assetDescriptionList'][i].replace('\n', ' '),
                    'subholdingOf': data['assetSubholdingOf'][i].replace('\n', ' ')
                },
                type=data['transactionTypeList'][i].replace('\n', ' '),
                filingDate=data['datesList'][i][0].replace('\n', ' '),
                notificationDate=data['datesList'][i][1].replace('\n', ' '),
                amount=data['amountList'][i].replace('\n', ' '),
            )
            self.transactions.append(newTransaction)

        Report.collection.append(self)

    def __eq__(self, other):
        # Check document ID first
        if self.docID != other.docID:
            return False
        # Check if other properties are equal
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        outputStr = f'\nID: {self.docID}\nName: {self.name}\nState/District: {self.stateDistrict}\n'
        count = 1
        for transaction in self.transactions:
            outputStr += '\n******************************\n'
            outputStr += f'\nTransaction {count}: \n{transaction}'
            count += 1
        outputStr += '\n******************************\n'
        return outputStr

    def convertToJSON(self):
        return {
            'docID': self.docID,
            'name': self.name,
            'stateDistrict': self.stateDistrict,
            'year': self.year,
            'messageFlags': self.messageFlags,
            'transactions': [transaction.convertToJSON() for transaction in self.transactions]
        }

    def getURL(self):
        # If docID begins with 2, use:
        # https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{self.year}/{self.docID}.pdf
        # Else use:
        # https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{self.year}/{self.docID}.pdf
        if self.docID.startswith('2'):
            return f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{self.year}/{self.docID}.pdf'
        else:
            return f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{self.year}/{self.docID}.pdf'

    def createReportFromString(self, extractedText, year = datetime.now().year):
        self.messageFlags = []

        self.docID = re.search('(?<=Filing ID #)\d+', extractedText, re.IGNORECASE).group()
        self.name = re.search('(?<=Status:)(?:\\n)+([\w. ]+)', extractedText).group(1)
        self.stateDistrict = re.search('(?<=State\/District:\s)[\d\w]+', extractedText).group()

        # Transactions
        data = {}

        data['assetTitleList'] = []
        # Replace every single instance of \n (NOT \n\n) with single space. Helps with regex.
        regExp = re.compile('(?<!(?:\\n))(?:\\n)(?!(?:\\n))')
        extractedTextModified = regExp.sub(' ', extractedText)
        # Find every text between \n\n and \n\n
        matchList = re.findall('(?<=(?:\\n){2}).+?(?=(?:\\n){2})', extractedTextModified)
        for match in matchList:
            # If str ends with '[NN]', where N is any uppercase letter, add rest of string to asset title list
            searchMatch = re.search('.+?(?=(?:\\n)|\s\[[A-Z]{2}\])', match)
            if searchMatch is not None:
                data['assetTitleList'].append(searchMatch.group())

        # Use non-modified extracted text. Could change in future to only use matchList

        data['ownerList'] = re.findall('(?<=(?:\\n){2})[A-Z]{2}(?=(?:\\n){2})', extractedText) # Full match, no capture group
        # Remove any matches of 'ID'
        data['ownerList'] = [ owner for owner in data['ownerList'] if owner != 'ID' ]

        data['assetTypeCodeList'] = re.findall('(?<=\[)[a-zA-Z]+?(?=(?=\]\\n){2}|\]\s)', extractedText) # Full match, no capture group
        # Convert to uppercase (case where letter is parsed as lower but should be upper)
        data['assetTypeCodeList'] = [ typeCode.upper() for typeCode in data['assetTypeCodeList'] ]

        # Asset should include either a description or subholding of. Have only seen reports with one or the other.
        data['assetDescriptionList'] = re.findall('(?<=description:\s).+?(?=(?:\\n){2})', extractedText, re.IGNORECASE) # Full match, no capture group
        data['assetSubholdingOf'] = re.findall('(?<=subholding\sof:\s).+?(?=(?:\\n){2})', extractedText, re.IGNORECASE)

        data['assetFilingStatusList'] = re.findall('(?<=filing\sstatus: ).+?(?=(?:\\n))', extractedText, re.IGNORECASE) # Full match, no capture group
        data['transactionTypeList'] = re.findall('(?<=(?:\\n){2}|\] )[A-Z](?: \(partial\))?(?=(?:\\n){2})', extractedText) # Full match, no capture groups
        data['datesList'] = re.findall('(?<=(?:\\n){2})([\d\/]+)\s([\d\/]+)(?=(?:\\n){2})', extractedText) # Two capture groups
        data['amountList'] = re.findall('\$[\d,]+?\s-(?:\\n)*\s*\$[\d,]+?(?=(?:\\n){2})', extractedText) # Full match, no capture group

        # Check for missing values that weren't captured

        nTransactions = statistics.mode([len(data[key]) for key in data])

        # Do NOT check owner list (most often left blank)
        # Do NOT check description or subholdingOf (could have one, both, or none)
        keysToSkip = ['ownerList', 'assetDescriptionList', 'assetSubholdingOf']
        
        for key, list in data.items():
            if len(list) < nTransactions:
                if key not in keysToSkip:
                    # Add message flag
                    self.messageFlags.append(f'{key} has missing values!')
                    print(f'{key} has missing values!')
                # Change list length to match nTransactions using empty string as value
                list.extend(['' for i in range(nTransactions - len(list))])
            elif len(list) > nTransactions:
                if key not in keysToSkip:
                    # Add message flag
                    self.messageFlags.append(f'{key} has too many values!')
                    print(f'{key} has too many values!')

        self.transactions = []
        for i in range(nTransactions):
            newTransaction = Transaction(
                owner=data['ownerList'][i].replace('\n', ' '),
                asset={
                    'title': data['assetTitleList'][i].replace('\n', ' '), 
                    'typeCode': data['assetTypeCodeList'][i].replace('\n', ' '), 
                    'filingStatus': data['assetFilingStatusList'][i].replace('\n', ' '), 
                    'description': data['assetDescriptionList'][i].replace('\n', ' '),
                    'subholdingOf': data['assetSubholdingOf'][i].replace('\n', ' ')
                },
                type=data['transactionTypeList'][i].replace('\n', ' '),
                filingDate=data['datesList'][i][0].replace('\n', ' '),
                notificationDate=data['datesList'][i][1].replace('\n', ' '),
                amount=data['amountList'][i].replace('\n', ' '),
            )
            self.transactions.append(newTransaction)

        Report.addToCollection(self)

    def createReportFromJSON(self, jsonObj):
        self.messageFlags = jsonObj['messageFlags']

        self.docID = jsonObj['docID']
        self.name = jsonObj['name']
        self.stateDistrict = jsonObj['stateDistrict']
        self.year = jsonObj['year']

        self.transactions = []
        for transaction in jsonObj['transactions']:
            newTransaction = Transaction(
                owner=transaction['owner'],
                asset={
                    'title': transaction['asset']['title'], 
                    'typeCode': transaction['asset']['typeCode'], 
                    'filingStatus': transaction['asset']['filingStatus'], 
                    'description': transaction['asset']['description'],
                    'subholdingOf': transaction['asset']['subholdingOf'],
                },
                type=transaction['type'],
                filingDate=transaction['filingDate'],
                notificationDate=transaction['notificationDate'],
                amount=transaction['amount'],
            )

            self.transactions.append(newTransaction)

        Report.addToCollection(self)

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