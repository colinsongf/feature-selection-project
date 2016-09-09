import definitions
import numpy as np

class Darwin(object):
	def __init__(self, populationSize):
		self.population = []
		self.initializePopulation(populationSize)


	def initializePopulation(self, populationSize):
		for i in range(0, populationSize):
			newIndividual = [0] * len(definitions.selectors) * len(definitions.classifiers)
			
			selectedFeatureNumber = np.random.randint(0, len(definitions.selectors) - 1)
			newIndividual[selectedFeatureNumber] = 1

