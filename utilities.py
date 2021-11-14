
class TestBaseClass:
    collection = []
    def __init__(self):
        TestBaseClass.addToCollection(self)

    @classmethod
    def addToCollection(cls, obj):
        cls.collection.append(obj)

class TestChildClass01(TestBaseClass):
    def __init__(self, number):
        super(TestChildClass01, self).__init__()
        self.number = number

class TestChildClass02(TestBaseClass):
    def __init__(self, letter):
        super(TestChildClass02, self).__init__()
        self.letter = letter

def main():
    # Create two TestChildClass01 instances
    firstChild01 = TestChildClass01(0)
    secondChild01 = TestChildClass01(1)

    # Create two TestChildClass02 instances
    firstChild02 = TestChildClass02('a')
    secondChild02 = TestChildClass02('b') 

    print(TestChildClass01.collection)
    print(TestChildClass02.collection)

if __name__ == '__main__':
    main()