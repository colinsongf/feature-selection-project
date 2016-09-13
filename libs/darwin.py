import numpy as np
from operator import itemgetter
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from . import array_handler, constants, definitions, dicts as customDicts, file_manager_module as fmm
from FeatureSelectionMethods.T_Statistics import T_Statistics

class Darwin(object):
	def __init__(self, trainingFile, testFile, populationSize, maxNumberOfFeatures, maxIter):
		self.trainingFile = trainingFile
		self.testFile = testFile

		self.maxIter = maxIter

		self.populationSize = populationSize
		self.maxNumberOfFeatures = maxNumberOfFeatures
		self.population = []
		self.firstGeneration = True


	# Cria um invidivíduo aleatório
	def createRandomIndividual(self):
		newIndividual = dict(customDicts.gene)
		newIndividual['trainingFile'] = self.trainingFile
		newIndividual['testFile'] = self.testFile
		newIndividual['selectionMethod'] = definitions.selectors[np.random.randint(0, len(definitions.selectors)-1, dtype='int')]
		newIndividual['numberOfSelectedFeatures'] = np.random.randint(1, self.maxNumberOfFeatures + 1, dtype='int')
		newIndividual['classificationMethod'] = definitions.classifiers[np.random.randint(0, len(definitions.classifier)-1, dtype='int')]
		newIndividual['accuracy'] = None


	# Cria um determinado indivíduo
	def createDeterminedIndividual(self, selectionMethod, numberOfSelectedFeatures, classificationMethod):
		newIndividual = dict(customDicts.gene)
		newIndividual['trainingFile'] = self.trainingFile
		newIndividual['testFile'] = self.testFile
		newIndividual['selectionMethod'] = selectionMethod
		newIndividual['numberOfSelectedFeatures'] = numberOfSelectedFeatures
		newIndividual['classificationMethod'] = classificationMethod
		newIndividual['accuracy'] = None


	# Cria a população inicial
	def initializePopulation(self):
		for p in range(self.populationSize):
			self.population.append(self.createRandomIndividual())


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


	# Troca informação genética -> swap simples entre os indivíduos sorteados
	# Gene[selectionMethod]
	# Gene[numberOfSelectedFeatures]
	# Gene[classificationMethod]
	def crossover(self):
		previousPopulationSize = len(self.population)

		for i in range(self.populationSize - previousPopulationSize):
			parent1 = self.population[np.random.randint(previousPopulationSize), dtype='int']
			parent2 = self.population[np.random.randint(previousPopulationSize), dtype='int']

			# Faz a média do número de características dos pais
			childNumberOfFeatures = int( (parent1['numberOfSelectedFeatures'] + parent2['numberOfSelectedFeatures']) / 2)
			if(childNumberOfFeatures < 1):
				childNumberOfFeatures = 1
			
			if(np.random.randint(2) == 0):
				child = self.createDeterminedIndividual(parent1['selectionMethod'], childNumberOfFeatures, parent2['classificationMethod'])
			else:
				child = self.createDeterminedIndividual(parent2['selectionMethod'], childNumberOfFeatures, parent1['classificationMethod'])

			if(np.random.randint(100, dtype='int') <= definitions.probMutation):
				mutate(child)

			self.population.append(child)


	# Muta o método de seleção
	def mutateSelectionMethod(self, individual):
		if( definitions.selectors.index(individual['selectionMethod']) == (len(definitions.selectors)-1) ):
			individual['selectionMethod'] = definitions.selectors[0]
		else:
			individual['selectionMethod'] = definitions.selectors[definitions.selectors.index(individual['selectionMethod']) + 1]

	# Muta o método de classificação
	def mutateClassificationMethod(self, individual):
		if( definitions.classifiers.index(individual['classificationMethod']) == (len(definitions.classifiers)-1) ):
			individual['classificationMethod'] = definitions.classifiers[0]
		else:
			individual['classificationMethod'] = definitions.classifiers[definitions.classifiers.index(individual['classificationMethod']) + 1]


	# Faz a mutação ou no método de seleção ou no método de classificação
	# Estratégia de "Pegue o próximo"
	def mutate(self, individual):
		# Se existem mais de um método de seleção e mais de um de classificação disponíveis, escolha mutar um (50% de chance para cada)
		if(len(definitions.selectors) > 1 and len(definitions.classifiers) > 1):
			if(np.random.randint(2, dtype='int') == 0):
				self.mutateSelectionMethod(individual)
			else:
				self.mutateClassificationMethod(individual)

		# Se existe mais de um método apenas de seleção
		elif(len(definitions.selectors) > 1):
			# Muta o método de seleção
			self.mutateSelectionMethod(individual)

		# Se existe mais de um método apenas de classificação
		elif(len(definitions.classifiers) > 1):
			# Muta o método de classificação
			self.mutateClassificationMethod(individual)


	def getResults(self):
		fittest = self.population[0]
		fittestIndividuals = [fittest]

		for i in range(1, len(self.population)):
			if(self.population[i]['accuracy'] == fittest):
				fittestIndividuals.append(self.population[i])

		return fittestIndividuals


	def run(self):
		if(self.firstGeneration):
			self.initializePopulation()

		for i in range(self.maxIter):
			self.evaluate()
			self.selectFittestIndividuals()
			# Crossover and mutate
			self.crossover()

		print('Fittest individuals:\n{}'.format(self.getResults()))