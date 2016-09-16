# coding=utf-8

import os
import file_manager_module as fmm
import constants
import definitions
from libs.dicts import resultadoSelecao
import libs.array_handler as ah
from libs.FeatureSelectionMethods.T_Statistics import T_Statistics
from operator import itemgetter

class SelectionModule(object):

	# ATTR #
	numberOfCl = None


	def __init__(self, numberOfCl=1):
		if(numberOfCl is None or numberOfCl < 0):
			raise Exception("Invalid NUMBER OF CLASSIFICATORS to classify")
		
		self.numberOfCl = numberOfCl


	def writeResults(self, results):
		if(not os.path.isdir(constants.resultsDirPath)):
			os.makedirs(constants.resultsDirPath)

		resultFile = open(constants.resultsDirPath + '/' + constants.resultsSelectionFileName, 'w')

		for r in results:
			resultFile.write('{};{};{};{};{};{}\n'.format(r['arquivo'], r['amostra'], r['comparacao'], r['nomeArquivo'], r['metodo'],','.join(str(d) for d in r['indices'])))

		resultFile.close()
		

	def writeNewFile(self, fileName, resourceFile, result, inputData, inputLabels):
		filePath = constants.newFilesPath + '/' + result['metodo'] + '/' + result['amostra'] + '/' + result['comparacao']
		
		# Armazena apenas as colunas selecionadas
		outputData = []
		for row in inputData:
			outputData.append(itemgetter(*result['indices'])(row))
		
		if(not os.path.isdir(filePath)):
			os.makedirs(filePath)
		
		# Escreve o arquivo
		newFile = open(filePath + '/' + fileName, 'w')
		for i in range(0, len(outputData)):
			newFile.write('{} {}\n'.format(' '.join(str(o) for o in outputData[i]), inputLabels[i]))
		newFile.close()
		
		# "Avisa" a existência do novo arquivo no arquivo de RESOURCE
		resourceFile.write(filePath + '/' + fileName + '\n')


	def writeNewTrainingFile(self, result, resTrainingFile):
		(inputData, inputLabels) = fmm.getInputDataFromFile(result['arquivo'])
			
		# Escreve o novo arquivo
		fileName = result['nomeArquivo'][0 : result['nomeArquivo'].index('.')] + '.txt'
		self.writeNewFile(fileName, resTrainingFile, result, inputData, inputLabels)


	def writeNewTestFile(self, result, resTestFile):
		fileIndex = result['nomeArquivo'][(result['nomeArquivo'].index('_') + 1) : result['nomeArquivo'].index('.')]
		
		inputTestFile = constants.dataPath + '/' + result['amostra'] + '/' + result['comparacao'] + '/Teste_' + fileIndex + constants.fileExtension
		(inputData, inputLabels) = fmm.getInputDataFromFile(inputTestFile)
		
		# Escreve o novo arquivo
		fileName = 'Teste_' + fileIndex + '.txt'
		self.writeNewFile(fileName, resTestFile, result, inputData, inputLabels)


	def createNewFiles(self, selectionResults):
		if(not os.path.isdir(constants.resourcesDir)):
			os.makedirs(constants.resourcesDir)
			
		resTrainingFile = open(constants.resTrainingFiles, 'w')
		resTestFile = open(constants.resTestFiles, 'w')
		
		for result in selectionResults:
			self.writeNewTrainingFile(result, resTrainingFile)
			self.writeNewTestFile(result, resTestFile)

		resTrainingFile.close()
		resTestFile.close()
	
		
	def select(self, resultsList, data, labels, filePath, sample, comparison, usedFile):
		if(definitions.T_statistics):
			t_statistics = T_Statistics(data, labels)
			t_statistics.calculate()
			r = dict(resultadoSelecao)
			r['arquivo'] = filePath
			r['amostra'] = sample
			r['comparacao'] = comparison
			r['nomeArquivo'] = usedFile
			r['metodo'] = 'T_Statistics'
			r['indices'] = ah.getBestIndexes(t_statistics.getResult(), self.numberOfCl)
			resultsList.append(r)
		

	def run(self):
		print("SELECT >> Starting feature selection process...")
		results = []
		samples = fmm.getSamplesName(constants.dataPath)

		for sample in samples:
			comparisons = fmm.getComparisonsNameFromSample(constants.dataPath, sample)

			for comparison in comparisons:
				files = fmm.getTrainingFilesNames(constants.dataPath, sample, comparison, constants.fileExtension)

				for f in files:
					filePath = constants.dataPath + '/' + sample + '/' + comparison + '/' + f
					(data, labels) = fmm.getInputDataFromFile(filePath)
					self.select(results, data, labels, filePath, sample, comparison, f)
					

		self.writeResults(results)
		self.createNewFiles(results)

		print("SELECT >> Feature selection finished!")