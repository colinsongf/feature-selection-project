#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from operator import itemgetter
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from . import array_handler, constants, definitions, dicts as customDicts, file_manager_module as fmm
from FeatureSelectionMethods.T_Statistics import T_Statistics

class Darwin(object):
	
	def __init__(self):
		self.maxIter = definitions.numberOfGenerations
		self.populationSize = definitions.populationSize
		self.maxNumberOfFeatures = definitions.maxNumberOfSelectedFeatures
		self.population = []
		
		self.trainingFiles = fmm.getTrainingFilesPath()
		self.testFiles = fmm.getTestFilesPath()


	# Cria um invidivíduo aleatório
	def createRandomIndividual(self):
		newIndividual = dict(customDicts.gene)
		newIndividual['trainingFile'] = self.trainingFiles[np.random.randint(len(self.trainingFiles))]
		newIndividual['testFile'] = self.trainingFiles[np.random.randint(len(self.trainingFiles))]
		newIndividual['selectionMethod'] = definitions.selectors[np.random.randint(len(definitions.selectors))]
		newIndividual['numberOfSelectedFeatures'] = np.random.random_integers(1, self.maxNumberOfFeatures)
		newIndividual['classificationMethod'] = definitions.classifiers[np.random.randint(len(definitions.classifiers))]
		newIndividual['accuracy'] = None
		return newIndividual


	# Cria um determinado indivíduo
	def createDeterminedIndividual(self, trainingFile, testFile, selectionMethod, numberOfSelectedFeatures, classificationMethod):
		newIndividual = dict(customDicts.gene)
		newIndividual['trainingFile'] = trainingFile
		newIndividual['testFile'] = testFile
		newIndividual['selectionMethod'] = selectionMethod
		newIndividual['numberOfSelectedFeatures'] = numberOfSelectedFeatures
		newIndividual['classificationMethod'] = classificationMethod
		newIndividual['accuracy'] = None
		return newIndividual


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
			(training_data, training_labels) = fmm.getInputDataFromFile(individual['trainingFile'])
			(test_data, test_labels) = fmm.getInputDataFromFile(individual['testFile'])

			selectedFeaturesIndexes = self.selectFeatures(individual)

			# Guarda apenas as colunas selecionadas
			training_data = array_handler.getColumns2DList(training_data, selectedFeaturesIndexes)
			test_data = array_handler.getColumns2DList(test_data, selectedFeaturesIndexes)

			# Classifica e armazena o resultado obtido
			individual['accuracy'] = self.classify(individual, training_data, training_labels, test_data, test_labels)


	# Seleciona os indivíduos mais aptos
	def selectFittestIndividuals(self):
		numberOfFittest = int(definitions.naturalSelectionThreshold * len(self.population))
		fittestIndividuals = sorted(self.population, key=itemgetter('accuracy'), reverse=True)[0:numberOfFittest]
		self.population = fittestIndividuals
		print("\tFittest: {}".format(self.population[0]['accuracy']))
		
	
	# Método de torneio
	# Retorna o indivíduo que produzir o maior grau de acurácia
	# Caso haja empate, considera o que utilizou a menor quantidade de características
	def tournment(self, individual1, individual2):
		if(individual1['accuracy'] > individual2['accuracy']):
			return individual1
		elif(individual2['accuracy'] > individual1['accuracy']):
			return individual2
		else:
			if(individual1['numberOfSelectedFeatures'] < individual2['numberOfSelectedFeatures']):
				return individual1
			else:
				return individual2
		
		
	# Seleciona pais para a próxima geração
	def getParent(self):
		# Pega dois individuos distintos
		individual1 = self.population[np.random.randint(len(self.population))]
		individual2 = self.population[np.random.randint(len(self.population))]

		# Garante que são indivíduos distintos		
		while(individual2 == individual1):
			individual2 = self.population[np.random.randint(len(self.population))]
			
		# Retorna o mais apto
		return self.tournment(individual1, individual2)


	# Troca de informação genética entre indivíduos selecionados aleatoriamente
	# e indicados para serem pais da próxima geração através do método de torneio:
	# avalia-se quem tem a maior acurácia
	def crossover(self):
		nNewChildren = self.populationSize - len(self.population)

		mutatedChildren = 0
		
		for i in range(nNewChildren):
			parent1 = self.getParent()
			parent2 = self.getParent()
			
			while(parent2 != parent1):
				parent2 = self.getParent()

			# TODO: implementar PANDAS na população para tornar mais fácil a troca de informação genética
			# Faz a média do número de características dos pais
			childNumberOfFeatures = int( (parent1['numberOfSelectedFeatures'] + parent2['numberOfSelectedFeatures']) / 2)
			if(childNumberOfFeatures < 1):
				childNumberOfFeatures = 1
			
			if(np.random.random_integers(1) == 0):
				child = self.createDeterminedIndividual(parent1['selectionMethod'], childNumberOfFeatures, parent2['classificationMethod'])
			else:
				child = self.createDeterminedIndividual(parent2['selectionMethod'], childNumberOfFeatures, parent1['classificationMethod'])

			if(np.random.random() <= definitions.initialProbMutation):
				if(self.mutate(child)):
					mutatedChildren += 1

			self.population.append(child)
		
		mutationRate = float(mutatedChildren) / float(nNewChildren)
		print("\tMutations rate: {0:.2f}%".format(mutationRate * 100))


	# Faz a mutação ou no método de seleção ou no método de classificação
	# Estratégia de "Pegue o próximo"
	def mutate(self, individual):
		# Se existem mais de um método de seleção E mais de um de classificação disponíveis, escolha mutar um (50% de chance para cada)
		if(len(definitions.selectors) > 1 and len(definitions.classifiers) > 1):
			if(np.random.random_integers(1) == 0):
				individual['selectionMethod'] = definitions.selectors[np.random.randint(len(definitions.selectors))]
				return True
			else:
				individual['classificationMethod'] = definitions.classifiers[np.random.randint(len(definitions.classifiers))]
				return True

		# Se existe mais de um método apenas de seleção
		elif(len(definitions.selectors) > 1):
			# Muta o método de seleção
			individual['selectionMethod'] = definitions.selectors[np.random.randint(len(definitions.selectors))]
			return True

		# Se existe mais de um método apenas de classificação
		elif(len(definitions.classifiers) > 1):
			# Muta o método de classificação
			individual['classificationMethod'] = definitions.classifiers[np.random.randint(len(definitions.classifiers))]
			return True
			
		return False


	def getResults(self):
		fittest = self.population[0]
		fittestIndividuals = [fittest]

		for i in range(1, len(self.population)):
			# Se os individuos possuem a mesma acuracia
			if(self.population[i]['accuracy'] == fittest['accuracy']):
				# Mas são elementos distintos
				if(fittest != self.population[i]['accuracy']):
					fittestIndividuals.append(self.population[i])
				
				
		resultDf = pd.DataFrame(fittestIndividuals)

		return resultDf


	def run(self):
		print("\n> Initializing population..."),
		self.initializePopulation()
		print("OK!")

		print("> Starting iterations...")
		for i in range(self.maxIter):
			print("Iteration {}: Running...".format(i))
			self.evaluate()
			self.selectFittestIndividuals()
			# Crossover and mutate
			self.crossover()
			print("Iteration {}: Done!\n".format(i))

		print('\nFittest individuals:\n{}'.format(self.getResults()))