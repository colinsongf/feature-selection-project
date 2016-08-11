# coding=utf-8

import os
import string
import numpy as np
from libs.FeatureSelectionMethods.CapacityAnalysis import CapacityAnalysis
import file_manager_module as fmm
from ResultadoSelecao import ResultadoSelecao

class SelectionProcess(object):

	# ATTR #
	dataPath 				= '/home/eduardo/Documentos/Pos-Graduacao/Trabalho mestrado/Dados/WFS'
	resultsDirPath			= os.getcwd() + '/results'
	newFilesPath			= os.getcwd() + '/newFiles'
	filesToClassifyFile		= os.getcwd() + '/resources/filesToClassify.txt'
	fileExtension 			= '.arff'
	numberOfCl				= None
	saveResults				= True


	def __init__(self, numberOfCl=1, dataPath=None, fileExtension=None, saveResults=True):
		if(numberOfCl is None or numberOfCl <= 0):
			raise Exception("Invalid NUMBER OF CLASSIFICATORS to select")
		self.numberOfCl = numberOfCl

		if(dataPath is not None):
			self.dataPath = dataPath

		if(fileExtension is not None):
			if('.' not in fileExtension):
				fileExtension = '.' + fileExtension

			self.fileExtension = fileExtension
		
		self.saveResults = saveResults


	def writeNewFiles(self, selectionResults):
		if(not os.path.isdir(self.newFilesPath)):
			os.makedirs(self.newFilesPath)

		fClassify = open(self.filesToClassifyFile, 'w')
		for result in selectionResults:
			fileAnalisedIndex = result.getFileUsed()[(result.getFileUsed().index("_")+1) : result.getFileUsed().index(".")]
			testFileName = "Teste_" + fileAnalisedIndex + self.fileExtension
			existingTestFilePath = self.dataPath + "/" + result.getSample() + "/" + result.getComparison() + "/" + testFileName

			if(os.path.exists(existingTestFilePath)):
				filePath = self.newFilesPath + '/' + result.getSample() + '/' + result.getComparison()
				if(not os.path.isdir(filePath)):
					os.makedirs(filePath)

				print("Writing FILE: {}...".format(filePath + "/" + testFileName)),

				fClassify.write('{}\n'.format(filePath + "/" + testFileName))

				(matA, matB, labels) = fmm.getInputDataFromFile(existingTestFilePath)

				selectedIndexes = result.getResultadoSelecao()
				selectedIndexes = selectedIndexes[0:self.numberOfCl]

				matA = np.take(matA, selectedIndexes, axis=1)
				matB = np.take(matB, selectedIndexes, axis=1)

				matA = matA.tolist()
				matB = matB.tolist()

				linesToWrite = []
				# @relation
				linesToWrite.append('@relation \'{}\''.format(testFileName))
				linesToWrite.append('')
				# @attribute x0 real
				for i in range(0, len(selectedIndexes)):
					linesToWrite.append('@attribute\tx{}\treal'.format(i+1))
				linesToWrite.append('')
				# @attribute class {1, 2}
				linesToWrite.append('@attribute\tclass\t{}{}{}'.format('{', ', '.join(labels), '}'))
				linesToWrite.append('')
				# @data
				linesToWrite.append('@data')
				''' 
				!!!!! TODO REMOVER HARDCODED DAS LABELS !!!!!
				'''
				# DADOS
				for row in matA:
					row.append(labels[0])
					linesToWrite.append(' '.join(str(c) for c in row))
				for row in matB:
					row.append(labels[1])
					linesToWrite.append(' '.join(str(c) for c in row))

				f = open(filePath + '/' + testFileName, 'w')
				for line in linesToWrite:
					f.write(line + '\n')
				f.close()
				print("OK")

			else:
				print("FILE DOES NOT EXISTS! : " + existingTestFilePath)

		fClassify.close()


	'''
	Escreve as linhas no arquivo utilizando o formato:
	[filePath];[amostra];[comparacao];[nomeDoArquivoUsado];[indices,]\n
	'''
	def writeResults(self, results):
		print("Writing results..."),
		if(not os.path.isdir(self.resultsDirPath)):
			os.makedirs(self.resultsDirPath)

		'''
		!!!!! REMOVER HARDCODED !!!!!
		'''
		fileName = 'selection.txt'
		resultsFilePath = self.resultsDirPath + '/' + fileName

		resultFile = open(resultsFilePath, 'w')

		for r in results:
			resultFile.write('{};{};{};{};{}\n'.format(r.getFilePath(), r.getSample(), r.getComparison(), r.getFileUsed(), ','.join(str(d) for d in r.getResultadoSelecao())))

		resultFile.close()
		print("OK")


	def run(self):
		print(">> RUNNING SELECTION SCRIPT")
		results = []

		samples = fmm.getSamplesName(self.dataPath)
		numSamples = len(samples)

		for sample in samples:
			print("Sample: {}".format(sample))
			comparisons = fmm.getComparisonsNameFromSample(self.dataPath, sample)
			numComparisons = len(comparisons)

			for comparison in comparisons:
				print("\tComparison: {}".format(comparison))
				files = fmm.getSemFilesNames(self.dataPath, sample, comparison, self.fileExtension)

				for f in files:
					print('\t\tFile: {}: '.format(f)),
					filePath = self.dataPath + '/' + sample + '/' + comparison + '/' + f
					[matA, matB] = fmm.getInputDataFromFile(filePath)
					capacidade = CapacityAnalysis(matA, matB)
					capacidade.calculate()
					result = ResultadoSelecao(filePath, sample, comparison, f, capacidade.getSortedIndexes())
					results.append(result)
					print('OK')
			print('')

		if(self.saveResults):
			self.writeResults(results)

		self.writeNewFiles(results)