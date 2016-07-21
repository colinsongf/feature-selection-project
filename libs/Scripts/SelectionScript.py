# coding=utf-8

import os
from natsort import natsorted
from libs.FeatureSelectionMethods import CapacityAnalysis
import libs.MyFunctions as myFunctions
from libs.MyClasses import ResultadoSelecao

class SelectionScript(object):

	# ATTR #
	dataPath 				= '/home/eduardo/Documentos/Pos-Graduacao/Trabalho mestrado/Dados/WFS'
	newFilesPath			= '/home/eduardo/Documentos/Pos-Graduacao/Trabalho mestrado/Dados/NewFiles'
	resultsDirPath			= os.getcwd() + '/results/selection/'
	fileExtension 			= '.txt'
	saveResults				= True


	def __init__(self, dataPath=None, newFilesPath=None, fileExtension=None, saveResults=True):
		if(dataPath is not None):
			self.dataPath = dataPath

		if(newFilesPath is not None):
			if(not os.path.isdir(newFilesPath)):
				os.mkdir(newFilesPath)

			self.newFilesPath = newFilesPath

		if(fileExtension is not None):
			if('.' not in fileExtension):
				fileExtension = '.' + fileExtension

			self.fileExtension = fileExtension
		
		self.saveResults = saveResults


	def getSamplesName(self):
		return myFunctions.listAllDirFromPath(self.dataPath)


	def getSamplesDir(self):
		samplesDirs = getSamples

		for sampleDir in samplesDirs:
			sampleDir = self.dataPath + '/' + sampleDir

		return samplesDirs


	def getComparisonsNameFromSample(self, sample):
		return myFunctions.listAllDirFromPath(self.dataPath + '/' + sample + '/')


	def getSemFilesNames(self, sample, comparison, extension):
		path = self.dataPath + '/' + sample + '/' + comparison
		files = myFunctions.listAllFilesFromPathWithSubstring(path, extension)

		SemFiles = []
		for f in files:
			if 'Sem' in f:
				SemFiles.append(f)

		SemFiles = natsorted(SemFiles)
		return SemFiles


	def storeResults(self, results):
		if(not os.path.isdir(self.resultsDirPath)):
			os.makedirs(self.resultsDirPath)

		fileName = 'selection.txt'
		resultsFilePath = self.resultsDirPath + '/' + fileName

		resultFile = open(resultsFilePath, 'w')

		for r in results:
			resultFile.write('{};{};{};{}\n'.format(r.getSample(), r.getComparison(), r.getFileUsed(), ','.join(str(d) for d in r.getResultadoSelecao())))

		resultFile.close()


	def run(self):
		print(">> RUNNING SELECTION SCRIPT")
		results = []

		samples = self.getSamplesName()
		numSamples = len(samples)

		for sample in samples:
			print("Sample: {}".format(sample))
			comparisons = self.getComparisonsNameFromSample(sample)
			numComparisons = len(comparisons)

			for comparison in comparisons:
				print("\tComparison: {}".format(comparison))
				files = self.getSemFilesNames(sample, comparison, '.txt')

				for f in files:
					print('\t\tFile: {}: '.format(f)),
					filePath = self.dataPath + '/' + sample + '/' + comparison + '/' + f
					[matA, matB] = myFunctions.getMatrixesFromFile(filePath)
					capacidade = CapacityAnalysis(matA, matB)
					capacidade.calculate()
					result = ResultadoSelecao(sample, comparison, f, capacidade.getSortedIndexes())
					results.append(result)
					print('OK')
			print('')

		if(self.saveResults):
			self.storeResults(results)
