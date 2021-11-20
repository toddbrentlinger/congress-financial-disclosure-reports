class Animal:
	def __init__(self, nLegs):
		self.nLegs = nLegs
		
	def showLegs(self):
		print(f'I have {self.nLegs} legs!')
		
	def displayData(self):
		self.showLegs()

class FourLeggedAnimal(Animal):
	def __init__(self, footType):
		Animal.__init__(self, 4)
		self.footType = footType
		
	def showLegs(self):
		Animal.showLegs(self)
		print(f'My feet are type: {self.footType}')

cow = FourLeggedAnimal('hoof')
cow.showLegs()
cow.displayData()