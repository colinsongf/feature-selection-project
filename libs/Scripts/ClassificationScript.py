# coding=utf-8

import string
import weka.core.jvm as jvm
from weka.classifiers import Classifier, Evaluation
from weka.core.classes import Random
from weka.core.converters import Loader
from prettytable import PrettyTable
from libs.MyClasses import Classificador, ResultadoClassificacao
from libs.MyFunctions import setEncode


class ClassificationScript(object):

	# ATTR #
	classifiersFile 	= None
	dataFilesFile 		= None
	arffLoader 			= None
	classifierList 		= []
	dataFilenames 		= []
	resultList 			= []
	#Flag
	printResults		= None


	# METHODS #
	def __init__(self, classifiersFile, dataFilesFile, printResults=False):
		self.classifiersFile = classifiersFile
		self.dataFilesFile = dataFilesFile
		self.printResults = printResults


	def setup(self):
		self.arffLoader  = Loader(classname="weka.core.converters.ArffLoader")
		readDataPaths()
		readClassifiers()


	def readClassifiers(self):
		classificatorsFile = open(classifiersFile, 'r');
		aux = classificatorsFile.read()
		classificatorsFile.close()
		aux = aux.split()

		for classifierClassname in aux:
			classifierClassname = string.replace(classifierClassname, '/', '.')
			cSplit = classifierClassname.split('.')
			classifierClassname = ""
			for part in cSplit:
				if(part != 'class'):
					if(classifierClassname == ""):
						classifierClassname = part
					else:
						classifierClassname = classifierClassname + '.' + part

			cSplit = classifierClassname.split('.')
			classifierName = cSplit[len(cSplit)-1]

			self.classifierList.append(Classificador(classifierName, Classifier(classname=classifierClassname)))


	def readDataPaths(self):
		f = open(dataFilesFile, 'r')
		filePaths = f.read()
		f.close()
		filePaths = filePaths.split('\n')

		for filePath in filePaths:
			if filePath != '':
				self.dataFilenames.append(filePath)


	def evaluateClassifiers(self, data):
		classifiersResultList = []

		for classifier in self.classifierList:
			evaluation = Evaluation(data)
			evaluation.crossvalidate_model(classifier.wekaClassifier, data, 10, Random(1))

			#print(evaluation.summary())
			#print(evaluation.matrix())
			classifiersResultList.append([classifier.name, evaluation.percent_correct])

		return classifiersResultList


	def printResults(self):
		for result in self.resultList:
			table = PrettyTable(['Classificador', 'Acuracia'])

			for r in result.getResultados():
				table.add_row(r)

			print("ARQUIVO: " + result.getFilename())
			print(table)
			print


	def classify(self):
		for fileName in self.dataFilenames:
			data = self.arffLoader.load_file(fileName)
			data.class_is_last()
			
			resultado = ResultadoClassificacao(fileName, evaluateClassifiers(data))
			resultList.append(resultado)


	def run(self):
		setEncode()
		print("CLASSIFY >> STARTING"),
		jvm.start()
		print(" > OK")

		setup()
		classify()
		if(self.printResults):
			printResults()

		print("CLASSIFY >> STOPPING"),
		jvm.stop()
		print(" > OK")