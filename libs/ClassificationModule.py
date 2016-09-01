# coding=utf-8

import os
import string
import file_manager_module as fmm
import constants
import definitions
from sklearn import tree


class ClassificationModule(object):

	# ATTR #
	trainFiles			= []
	testFiles 			= []
	classifierList 		= []
	resultList 			= []


	# METHODS #
	def readDataPaths(self):
		# Lê os caminhos dos arquivos de treinamento
		f = open(constants.resTrainingFiles, 'r')
		
		lines = f.readlines()
		for l in lines:
			l = string.strip(l)
			if l:
				self.trainFiles.append(l)

		f.close()
		
		# Lê os caminhos dos arquivos de teste
		f = open(constants.resTestFiles, 'r')
		
		lines = f.readlines()
		for l in lines:
			l = string.strip(l)
			if l:
				self.testFiles.append(l)

		f.close()


	def classify(self):
		if(len(self.trainFiles) == len(self.testFiles)):
			for i in range(0, len(self.trainFiles)):
				# Pega os dados dos arquivos de treinamento e teste
				(trainingData, trainingLabels) = fmm.getInputDataFromFile(self.trainFiles[i])
				(testData, testLabels) = fmm.getInputDataFromFile(self.testFiles[i])

				if(definitions.DecisionTree):
					# Treina o classificador
					clf = tree.DecisionTreeClassifier()
					clf = clf.fit(trainingData, trainingLabels)
					# Classifica os arquivos de teste
					self.resultList.append([self.testFiles[i], clf.score(testData, testLabels)])
	
	
	def writeResults(self):
		if(not os.path.isdir(constants.resultsDirPath)):
			os.makedirs(constants.resultsDirPath)

		f = open(constants.resultsDirPath + '/' + constants.resultsClassificationFileName, 'w')

		for result in self.resultList:
			f.write('{};{}\n'.format(result[0], result[1]))
		
		f.close()


	def run(self):
		print("CLASSIFY >> Starting classification... ")

		self.readDataPaths()
		self.classify()
		self.writeResults()

		print("CLASSIFY >> Classification finished!")