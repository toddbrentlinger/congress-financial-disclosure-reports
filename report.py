import re
from transaction import Transaction

class Report:
    def __init__(self, extractedText):
        self.docID = re.search('Filing ID #(\d+)', extractedText).group(1)
        self.name = re.search('Status:(?:\\n)+([\w. ]+)', extractedText).group(1)
        self.stateDistrict = re.search('State\/District: ([\d\w]+)', extractedText).group(1)

    def __str__(self):
        return f'Filing Date: {self.docID}\nName: {self.name}\nState/District: {self.stateDistrict}\n'