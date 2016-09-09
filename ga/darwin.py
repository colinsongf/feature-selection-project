import numpy as np

class Darwin(object):
	def __init__(self, populationSize):
		self.population = []
		self.initializePopulation(populationSize)


	def initializePopulation(self, populationSize):
		for i in range(0, populationSize):
			self.population.append(np.random.randint(2, size=populationSize))