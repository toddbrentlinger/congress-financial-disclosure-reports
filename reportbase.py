import json
from json.decoder import JSONDecodeError

class ReportBase:
    collection = []
    jsonFile = ''

    def __init__(self, docID, filingDate):
        self.docID = docID
        self.filingDate = filingDate

    def __eq__(self, other):
        # Check document ID first
        if self.docID != other.docID:
            return False
        # Check if other properties are equal
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

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
            except JSONDecodeError:
                pass

    @classmethod
    def addToCollection(cls, obj):
        # Check if obj is correct type
        # Check if obj already in collection
        if obj not in cls.collection:
            # Append to collection
            cls.collection.append(obj)
