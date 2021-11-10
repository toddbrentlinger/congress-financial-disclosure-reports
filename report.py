import re
from datetime import datetime
from transaction import Transaction

class Report:
    collection = []

    def __init__(self, extractedText, year = datetime.now().year):
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

        # User non-modified extracted text. Could change in future to only use matchList
        data['ownerList'] = re.findall('(?<=(?:\\n){2})[A-Z]{2}(?=\\n){2}', extractedText) # Full match, no capture group
        data['assetTypeCodeList'] = re.findall('(?<=\[)[A-Z]+?(?=(?=\]\\n){2}|\]\s)', extractedText) # Full match, no capture group
        data['assetDescriptionList'] = re.findall('(?<=DESCRIPTION:\s).+?(?=(?:\\n){2})', extractedText) # Full match, no capture group
        data['assetFilingStatusList'] = re.findall('(?<=filing\sstatus: ).+?(?=(?:\\n))', extractedText, re.IGNORECASE) # Full match, no capture group
        data['transactionTypeList'] = re.findall('(?<=(?:\\n){2}|\] )[A-Z](?: \(partial\))?(?=(?:\\n){2})', extractedText) # Full match, no capture groups
        data['datesList'] = re.findall('(?<=(?:\\n){2})([\d\/]+)\s([\d\/]+)(?=(?:\\n){2})', extractedText) # Two capture groups
        data['amountList'] = re.findall('\$[\d,]+?\s-(?:\\n)*\s*\$[\d,]+?(?=(?:\\n){2})', extractedText) # Full match, no capture group

        # Check for missing values that weren't captured
        nTransactions = max([len(data[key]) for key in data])
        for key, list in data.items():
            if len(list) < nTransactions:
                # Add message flag
                self.messageFlags.append(f'{key} has missing values!')
                # Change list length to match nTransactions
                list.extend(['' for i in range(nTransactions - len(list))])

        self.transactions = []
        for i in range(nTransactions):
            newTransaction = Transaction(
                owner=data['ownerList'][i].replace('\n', ' '),
                asset={
                    'title': data['assetTitleList'][i].replace('\n', ' '), 
                    'typeCode': data['assetTypeCodeList'][i].replace('\n', ' '), 
                    'filingStatus': data['assetFilingStatusList'][i].replace('\n', ' '), 
                    'description': data['assetDescriptionList'][i].replace('\n', ' '),
                },
                type=data['transactionTypeList'][i].replace('\n', ' '),
                date=data['datesList'][i][0].replace('\n', ' '),
                notificationDate=data['datesList'][i][1].replace('\n', ' '),
                amount=data['amountList'][i].replace('\n', ' '),
            )
            self.transactions.append(newTransaction)

        Report.collection.append(self)

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