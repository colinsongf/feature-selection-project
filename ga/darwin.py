import numpy as np
from . import gene_handler as gnh
from 

class Darwin(object):
	def __init__(self, populationSize, maxNumberOfFeatures):
		self.population = []
		self.maxNumberOfFeatures = maxNumberOfFeatures
		self.initializePopulation(populationSize)


	def initializePopulation(self, populationSize):
		for p in range(populationSize):
			self.population.append(gnh.generateIndividual(self.maxNumberOfFeatures))


	def evaluate(self):
