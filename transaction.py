
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

    def typeName(self):
        return Asset.typeCodeNames[self.typeCode]

class Transaction:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.owner = kwargs['owner']
        self.asset = kwargs['asset'] # use Asset object
        self.type = kwargs['type']
        self.date = kwargs['date'] # use Date object
        self.notificationDate = kwargs['notificationDate'] # use Date object
        self.amount = kwargs['amount']
        self.capGainsMoreThan200 = kwargs['capGainsMoreThan200']