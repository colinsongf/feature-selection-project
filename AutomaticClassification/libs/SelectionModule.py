# coding=utf-8

import os
import file_manager_module as fmm
import constants
from libs.FeatureSelectionMethods.CapacityAnalysis import CapacityAnalysis
from operator import itemgetter

resultadoSelecao = {
	'arquivo': None,
	'indices': None,
	'amostra': None,
	'comparacao': None,
	'nomeArquivo': None
}

class SelectionModule(object):

	# ATTR #
	numberOfCl = None


	def __init__(self, numberOfCl=1):
		if(numberOfCl is None or numberOfCl <= 0):
			raise Exception("Invalid NUMBER OF CLASSIFICATORS to select")
		
		self.numberOfCl = numberOfCl


	def writeResults(self, results):
		if(not os.path.isdir(constants.resultsDirPath)):
			os.makedirs(constants.resultsDirPath)

		resultFile = open(constants.resultsDirPath + '/' + constants.resultsSelectionFileName, 'w')

		for r in results:
			resultFile.write('{};{};{};{};{}\n'.format(r['arquivo'], r['amostra'], r['comparacao'], r['nomeArquivo'], ','.join(str(d) for d in r['indices'])))

		resultFile.close()


	def writeNewTrainingFile(self, result, resTrainingFile):
		(inputData, inputLabels) = fmm.getInputDataFromFile(result['arquivo'])
		
		# Armazena apenas as colunas selecionadas
		outputData = []
		for row in inputData:
			outputData.append(itemgetter(*result['indices'])(row))
			
		# Escreve o novo arquivo
		filePath = constants.newFilesPath + '/' + result['amostra'] + '/' + result['comparacao']
		fileName = result['nomeArquivo'][0 : result['nomeArquivo'].index('.')] + '.txt'
		
		if(not os.path.isdir(filePath)):
			os.makedirs(filePath)
		
		newTrainingFile = open(filePath + '/' + fileName, 'w')
		for i in range(0, len(outputData)):
			newTrainingFile.write('{} {}\n'.format(' '.join(outputData[i]), inputLabels[i]))
		newTrainingFile.close()
		
		# "Avisa" a existência do novo arquivo no arquivo de RESOURCE
		resTrainingFile.write(filePath + '/' + fileName + '\n')


	def writeNewTestFile(self, result, resTestFile):
		fileIndex = result['nomeArquivo'][(result['nomeArquivo'].index('_') + 1) : result['nomeArquivo'].index('.')]
		
		inputTestFile = constants.dataPath + '/' + result['amostra'] + '/' + result['comparacao'] + '/Teste_' + fileIndex + constants.fileExtension
		(inputData, inputLabels) = fmm.getInputDataFromFile(inputTestFile)
		
		# Armazena apenas as colunas selecionadas
		outputData = []
		for row in inputData:
			outputData.append(itemgetter(*result['indices'])(row))
		
		# Escreve o novo arquivo
		filePath = constants.newFilesPath + '/' + result['amostra'] + '/' + result['comparacao']
		fileName = 'Teste_' + fileIndex + '.txt'
		
		if(not os.path.isdir(filePath)):
			os.makedirs(filePath)
		
		newTestFile = open(filePath + '/' + fileName, 'w')
		for i in range(0, len(outputData)):
			newTestFile.write('{} {}\n'.format(' '.join(outputData[i]), inputLabels[i]))
		newTestFile.close()
		
		# "Avisa" a existência do novo arquivo no arquivo de RESOURCE
		resTestFile.write(filePath + '/' + fileName + '\n')


	def writeNewFiles(self, selectionResults):
		if(not os.path.isdir(constants.resourcesDir)):
			os.makedirs(constants.resourcesDir)
			
		resTrainingFile = open(constants.resTrainingFiles, 'w')
		resTestFile = open(constants.resTestFiles, 'w')
		
		for result in selectionResults:
			self.writeNewTrainingFile(result, resTrainingFile)
			self.writeNewTestFile(result, resTestFile)

		resTrainingFile.close()
		resTestFile.close()
		

	def run(self):
		print("SELECT >> Starting feature selection process...")
		results = []
		samples = fmm.getSamplesName(constants.dataPath)

		for sample in samples:
			comparisons = fmm.getComparisonsNameFromSample(constants.dataPath, sample)

			for comparison in comparisons:
				files = fmm.getSemFilesNames(constants.dataPath, sample, comparison, constants.fileExtension)

				for f in files:
					filePath = constants.dataPath + '/' + sample + '/' + comparison + '/' + f
					(data, labels) = fmm.getInputDataFromFile(filePath)
					
					capacidade = CapacityAnalysis(data, labels)
					capacidade.calculate()
					
					r = dict(resultadoSelecao)
					r['arquivo'] = filePath
					r['indices'] = capacidade.getBestIndexes(self.numberOfCl)
					r['amostra'] = sample
					r['comparacao'] = comparison
					r['nomeArquivo'] = f
					results.append(r)

		self.writeResults(results)
		self.writeNewFiles(results)

		print("SELECT >> Feature selection finished!")