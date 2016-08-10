# coding=utf-8

import os
import string
import weka.core.jvm as jvm
from weka.classifiers import Classifier, Evaluation
from weka.core.classes import Random
from weka.core.converters import Loader
import file_manager_module as fmm
from Classificador import Classificador
from ResultadoClassificacao import ResultadoClassificacao


class ClassificationProcess(object):

	# ATTR #
	classifiersFile 	= None
	filesToClassifyFile = None
	resultsDirPath 		= None
	arffLoader 			= None
	classifierList 		= []
	dataFilePaths 		= []
	resultList 			= []
	folds				= None


	# METHODS #
	def __init__(self, classifiersFile=None, filesToClassifyFile=None, resultsDirPath=None, folds=2):
		if classifiersFile is not None:
			self.classifiersFile = classifiersFile
		else:
			self.classifiersFile = os.getcwd() + '/resources/classifiersToUse.txt'

		if filesToClassifyFile is not None:
			self.filesToClassifyFile = filesToClassifyFile
		else:
			self.filesToClassifyFile = os.getcwd() + '/resources/filesToClassify.txt'

		if resultsDirPath is not None:
			self.resultsDirPath = resultsDirPath
		else:
			self.resultsDirPath = os.getcwd() + '/results'

		self.folds = folds


	def setup(self):
		self.arffLoader  = Loader(classname="weka.core.converters.ArffLoader")
		self.readDataPaths()
		self.readClassifiers()


	def readDataPaths(self):
		f = open(self.filesToClassifyFile, 'r')
		
		lines = f.readlines()
		for l in lines:
			l = string.strip(l)
			if l:
				self.dataFilePaths.append(l)

		f.close()


	def readClassifiers(self):
		classificatorsFile = open(self.classifiersFile, 'r');
		aux = classificatorsFile.read()
		classificatorsFile.close()
		aux = aux.splitlines()

		for classifierClassname in aux:
			classifierClassname = string.replace(classifierClassname, '/', '.')
			cSplit = classifierClassname.split('.')
			classifierClassname = ""
			for part in cSplit:
				if(part != "class"):
					if(classifierClassname == ""):
						classifierClassname = part
					else:
						classifierClassname = classifierClassname + '.' + part

			cSplit = classifierClassname.split('.')
			classifierName = cSplit[len(cSplit)-1]

			self.classifierList.append(Classificador(classifierName, Classifier(classname=classifierClassname)))


	def evaluateClassifiers(self, data):
		classifiersResultList = []

		for classifier in self.classifierList:
			evaluation = Evaluation(data)
			evaluation.crossvalidate_model(classifier.wekaClassifier, data, 2, Random(1))

			#print(evaluation.summary())
			#print(evaluation.matrix())
			classifiersResultList.append([classifier.name, evaluation.percent_correct])

		return classifiersResultList


	def classify(self):
		print("CLASSIFY >> CLASSIFYING...")
		for filePath in self.dataFilePaths:
			print("\tClassifying FILE: \'{}\'".format(filePath)),
			data = self.arffLoader.load_file(filePath)
			data.class_is_last()
			
			resultado = ResultadoClassificacao(filePath, self.evaluateClassifiers(data))
			self.resultList.append(resultado)
			print("OK")

		print("CLASSIFY >> CLASSIFYING... OK")


	'''
	Escreve os resultados no formato:
	[nomeDoArquivo];[resultados,]\n
	'''
	def writeResults(self):
		print("CLASSIFY >> WRITING RESULTS... "),
		if(not os.path.isdir(self.resultsDirPath)):
			os.makedirs(self.resultsDirPath)

		fileName = 'classification.txt'
		f = open(self.resultsDirPath + '/' + fileName, 'w')

		for result in self.resultList:
			f.write('{}'.format(result.fileName))

			for resultList in result.getResultados():
				f.write(';')
				numVirgulas = len(resultList) - 1
				virgula=1

				for data in resultList:
					f.write('{}'.format(data))
					if virgula <= numVirgulas:
						f.write(',')
					virgula = virgula+1

			f.write('\n')

		f.close()
		print("OK")


	def run(self):
		fmm.setEncode()
		print("CLASSIFY >> STARTING... "),
		jvm.start()
		print("OK")

		self.setup()
		self.classify()
		self.writeResults()

		print("CLASSIFY >> STOPPING"),
		jvm.stop()
		print(" > OK")