import numpy as np
from operator import itemgetter
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
#
from . import array_handler, constants, definitions, dicts as customDicts, file_manager_module as fmm
from FeatureSelectionMethods.T_Statistics import T_Statistics

class Darwin(object):
	def __init__(self, trainingFile, testFile, populationSize, maxNumberOfFeatures):
		self.trainingFile = trainingFile
		self.testFile = testFile

		self.populationSize = populationSize
		self.maxNumberOfFeatures = maxNumberOfFeatures
		self.population = []
		self.firstGeneration = True


	# Cria a população inicial
	def createPopulation(self, populationSize):
		for p in range(populationSize):
			newIndividual = dict(customDicts.gene)
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
	def selectFeatures(self, individual):
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
			(training_data_before, training_labels_before) = fmm.getInputDataFromFile(individual['trainingFile'])
			(test_data_before, test_labels_before) = fmm.getInputDataFromFile(individual['testFile'])

			selectedFeaturesIndexes = self.selectFeatures(individual)

			training_data_after = []
			training_labels_after = []
			test_data_after = []
			test_labels_after = []

			# Guarda apenas as colunas selecionadas
			for row in training_data_before:
				training_data_after.append(list(itemgetter(*selectedFeaturesIndexes)(row)))

			training_labels_after = list(itemgetter(*selectedFeaturesIndexes)(training_labels_before))

			for row in test_data_before:
				test_data_after.append(list(itemgetter(*selectedFeaturesIndexes)(row)))

			test_labels_after = list(itemgetter(*selectedFeaturesIndexes)(training_labels_before))


			# Classifica e armazena o resultado obtido
			individual['accuracy'] = self.classify(individual, training_data_after, training_labels_after, test_data_after, test_labels_after)


	# Seleciona os indivíduos mais aptos
	def selectFittestIndividuals(self):
		numberOfFittest = int(definitions.naturalSelectionThreshold * len(self.population))
		fittestIndividuals = sorted(self.population, key=itemgetter('accuracy'), reverse=True)[0:numberOfFittest]
		self.population = fittestIndividuals
		self.firstGeneration = False


	# Troca informação genética -> swap simples entre os indivíduos
	# Gene[selectionMethod]
	# Gene[numberOfSelectedFeatures]
	# Gene[classificationMethod]
	def crossover(self):
		