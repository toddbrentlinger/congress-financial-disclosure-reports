
class Asset:
    typeCodeNames = {
        "4K": "401K and Other Non-Federal Retirement Accounts",
        "5C": "529 College Savings Plan",
        "5P": "529 Prepaid Tuition Plan",
        "AB": "Asset-Backed Securities",
        "BA": "Bank Accounts, Money Market Accounts and CDs",
        "CO": "Collectibles",
        "CS": "Corporate Securities (Bonds and Notes)",
        "DB": "Defined Benefit Pension",
        "DO": "Debts Owed to the Filer",
        "DS": "Delaware Statutory Trust",
        "EF": "Exchange Traded Funds (ETF)",
        "EQ": "Excepted/Qualified Blind Trust",
        "ET": "Exchange Traded Notes",
        "FA": "Farms",
        "FE": "Foreign Exchange Position (Currency)",
        "FN": "Fixed Annuity",
        "FU": "Futures",
        "GS": "Government Securities and Agency Debt",
        "HE": "Hedge Funds & Private Equity Funds (EIF)",
        "HN": "Hedge Funds & Private Equity Funds (non-EIF)",
        "IC": "Investment Club",
        "IH": "IRA (Held in Cash)",
        "IP": "Intellectual Property & Royalties",
        "IR": "IRA",
        "MF": "Mutual Funds",
        "OI": "Ownership Interest (Holding Investments)",
        "OL": "Ownership Interest (Engaged in a Trade or Business)",
        "OP": "Options",
        "OT": "Other",
        "PE": "Pensions",
        "PS": "Stock (Not Publicly Traded)",
        "RE": "Real Estate Invest. Trust (REIT)",
        "RP": "Real Property",
        "SA": "Stock Appreciation Right",
        "ST": "Stocks (including ADRs)",
        "TR": "Trust",
        "VA": "Variable Annuity",
        "VI": "Variable Insurance",
        "WU": "Whole/Universal Insurance",
    }    

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.typeCode = kwargs['typeCode'] # use Asset.typeCodes dict to get asset name
        self.filingStatus = kwargs['filingStatus']
        self.description = kwargs['description']

    def __str__(self):
        return f'\nTitle: {self.title}\nType Code: {self.typeCode}\nFilingStatus: {self.filingStatus}\nDescription: {self.description}\n'

    def converToJSON(self):
        return {
            'title': self.title,
            'typeCode': self.typeCode,
            'filingStatus': self.filingStatus,
            'description': self.description
        }

    def typeName(self):
        return Asset.typeCodeNames[self.typeCode]

class Transaction:
    collection = []

    def __init__(self, id = '', owner = '', asset = {}, type = '', date = '', notificationDate = '', amount = '', capGainsMoreThan200 = ''):
        self.id = id
        self.owner = owner
        self.asset = Asset(title=asset['title'], typeCode=asset['typeCode'], filingStatus=asset['filingStatus'], description=asset['description'])
        self.type = type
        self.date = date # use Date object
        self.notificationDate = notificationDate # use Date object
        self.amount = amount
        self.capGainsMoreThan200 = capGainsMoreThan200

        Transaction.collection.append(self)

    def __str__(self):
        return f'Owner: {self.owner}\n\nAsset: {self.asset}\nType: {self.type}\nDate: {self.date}\nNotification Date: {self.notificationDate}\nAmount: {self.amount}\n'

    def convertToJSON(self):
        return {
            'id': self.id,
            'owner': self.owner,
            'asset': self.asset.converToJSON(),
            'type': self.type,
            'date': self.date.strftime('%m/%d/%Y'),
            'notificationDate': self.notificationDate.strftime('%m/%d/%Y'),
            'amount': self.amount,
            'capGainsMoreThan200': str(self.capGainsMoreThan200)
        }