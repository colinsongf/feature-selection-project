import numpy as np
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
#
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


	# Cria a população inicial
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


	# Seleciona as características de acordo com o método de seleção
	# apontado pelo gene do indivíduo e retorna os índices selecionados
	def select(self, individual):
		(data, labels) = fmm.getInputDataFromFile(individual['trainingFile'])

		if(individual['selectionMethod'] == constants.TStatistics):
			t_statistics = T_Statistics(data, labels)
			t_statistics.calculate()
			return array_handler.getBestIndexes(t_statistics.getResult(), individual['numberOfSelectedFeatures'])


	# Classifica de acordo com o método de classificação
	# apontado pelo gene do indivíduo e retorna a acurácia obtida
	def classify(self, individual, training_data, training_labels, test_data, test_labels):
		if(individual['classificationMethod'] == constants.DecisionTree):
			clf = tree.DecisionTreeClassifier()
		elif(individual['classificationMethod'] == constants.Lasso):
			clf = linear_model.Lasso(alpha = 0.1)
		elif(individual['classificationMethod']  == constants.SVM):
			clf = svm.SVC()
		elif(individual['classificationMethod']  == constants.GaussianNB):
			clf = GaussianNB()
		elif(individual['classificationMethod']  == constants.MultinomialNB):
			clf = MultinomialNB()
		elif(individual['classificationMethod']  == constants.BernoulliNB):
			clf = BernoulliNB()
		else:
			raise Exception("Invalid classifier!")
			exit()

		clf.fit(training_data, training_labels)
		return clf.score(test_data, test_labels)


	def evaluate(self):
		for individual in self.population:
			