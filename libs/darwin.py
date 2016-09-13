import numpy as np
from ... import definitions
from . import gene_handler as gnh, ClassificationModule as clfModule, constants, file_manager_module as fmm, array_handler, dicts
from FeatureSelectionMethods.T_Statistics import T_Statistics

class Darwin(object):
	def __init__(self, trainingFile, testFile, populationSize, maxNumberOfFeatures):
		self.trainingFile = trainingFile
		self.testFile = testFile
		self.population = []
		self.maxNumberOfFeatures = maxNumberOfFeatures
		self.initializePopulation(populationSize)


	def initializePopulation(self, populationSize):
		for p in range(populationSize):
			newIndividual = dict(dicts.gene)
			newIndividual['trainingFile'] = self.trainingFile
			newIndividual['testFile'] = self.testFile
			newIndividual['selectionMethod'] = np.random.randint(0, len(definitions.selectors))
			newIndividual['numberOfSelectedFeatures'] = np.random.randint(1, self.maxNumberOfFeatures + 1)
			newIndividual['classificationMethod'] = np.random.randint(0, len(definitions.classifier))
			newIndividual['accuracy'] = None
			#
			self.population.append(newIndividual)


	def select(self, individual):
		(data, labels) = fmm.getInputDataFromFile(individual['trainingFile'])

		if(individual['selectionMethod'] == constants.TStatistics):
			t_statistics = T_Statistics(data, labels)
			t_statistics.calculate()
			return array_handler.getBestIndexes(t_statistics.getResult(), individual['numberOfSelectedFeatures'])


	def classify(self, individual):
		


	def evaluate(self):
		