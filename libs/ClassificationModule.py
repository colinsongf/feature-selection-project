# coding=utf-8

import os
import string
import file_manager_module as fmm
import constants
import definitions
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB


class ClassificationModule(object):

	# ATTR #
	trainFiles		= []
	testFiles 		= []
	classifierList 	= []
	resultList 		= []


	# METHODS #
	def __init__(self):
		sel.readDataPaths();


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


	def fitAndAppendResult(self, fileIndex, clf, trainingData, trainingLabels, testData, testLabels, classifierLabel):
		# Treina o classificador
		clf.fit(trainingData, trainingLabels)
		# Classifica os arquivos de teste e guarda os resultados
		self.resultList.append([self.testFiles[fileIndex], classifierLabel, clf.score(testData, testLabels)])


	def classify(self):
		if(len(self.trainFiles) == len(self.testFiles)):
			for i in range(0, len(self.trainFiles)):
				# Pega os dados dos arquivos de treinamento e teste
				(trainingData, trainingLabels) = fmm.getInputDataFromFile(self.trainFiles[i])
				(testData, testLabels) = fmm.getInputDataFromFile(self.testFiles[i])

				if(definitions.DecisionTree):
					self.fitAndAppendResult(i, tree.DecisionTreeClassifier(), trainingData, trainingLabels, testData, testLabels, "DecisionTree")
					
				if(definitions.Lasso):
					self.fitAndAppendResult(i, linear_model.Lasso(alpha = 0.1), trainingData, trainingLabels, testData, testLabels, "Lasso")
					
				if(definitions.SVM):
					self.fitAndAppendResult(i, svm.SVC(), trainingData, trainingLabels, testData, testLabels, "SVM")
					
				if(definitions.GaussianNB):
					self.fitAndAppendResult(i, GaussianNB(), trainingData, trainingLabels, testData, testLabels, "GaussianNB")
					
				if(definitions.MultinomialNB):
					self.fitAndAppendResult(i, MultinomialNB(), trainingData, trainingLabels, testData, testLabels, "MultinomialNB")
					
				if(definitions.BernoulliNB):
					self.fitAndAppendResult(i, BernoulliNB(), trainingData, trainingLabels, testData, testLabels, "BernoulliNB")
	
	
	def writeResults(self):
		if(not os.path.isdir(constants.resultsDirPath)):
			os.makedirs(constants.resultsDirPath)

		f = open(constants.resultsDirPath + '/' + constants.resultsClassificationFileName, 'w')

		for result in self.resultList:
			# {arquivo_classificado};{classificador};{score}
			for i in range(0, len(result)):
				if i != (len(result)-1):
					f.write('{};'.format(result[i]))
				else:
					f.write('{}\n'.format(result[i]))
		
		f.close()


	def run(self):
		print("CLASSIFY >> Starting classification... ")

		self.readDataPaths()
		self.classify()
		self.writeResults()

		print("CLASSIFY >> Classification finished!")