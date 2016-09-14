import os
import string
from natsort import natsorted


def listAllFilesFromPathWithSubstring(path, substring):
	filePaths = []

	for _, _, files in os.walk(path):
		for f in files:
			if substring in f:
				filePaths.append(f)

	return filePaths


def listAllDirFromPath(path):
	dirs = []
	listdir = os.listdir(path)
	for d in listdir:
		if(os.path.isdir(path + '/' + d)):
			dirs.append(d)

	return dirs


def getSamplesName(dataPath):
	return listAllDirFromPath(dataPath)


def getComparisonsNameFromSample(dataPath, sample):
	return listAllDirFromPath(dataPath + '/' + sample + '/')


def getSemFilesNames(dataPath, sample, comparison, extension):
	path = dataPath + '/' + sample + '/' + comparison
	files = listAllFilesFromPathWithSubstring(path, extension)

	SemFiles = []
	for f in files:
		if 'Sem' in f:
			SemFiles.append(f)

	SemFiles = natsorted(SemFiles)
	return SemFiles


def getTesteFilesNames(dataPath, sample, comparison, extension):
	path = dataPath + '/' + sample + '/' + comparison
	files = listAllFilesFromPathWithSubstring(path, extension)

	TesteFiles = []
	for f in files:
		if 'Teste' in f:
			TesteFiles.append(f)

	TesteFiles = natsorted(TesteFiles)
	return TesteFiles


def getDataFromTxtFile(filePath):
	with open(filePath, 'r') as f:
		labels = []
		data = []

		linesRead = f.read().splitlines()
		for line in linesRead:
			valuesFromLine = line.split()
			
			# Converte os dados lidos para float
			valuesFromLine = [float(x) for x in valuesFromLine]
			labels = [float(x) for x in labels]
			
			# Armazena os dados
			data.append(valuesFromLine[0:(len(valuesFromLine)-1)])
			labels.append(valuesFromLine[len(valuesFromLine)-1])
			
		return data, labels


def getDataFromArffFile(filePath):
	f = open(filePath, 'r')

	inData = False

	labels = []
	data = []
	
	for line in f:
		if('@data' in line):
			inData = True
			continue

		if(inData == True and line != '\n'):
			row = line.split()
			for i in row:
				if i == '\n':
					row.remove(i)

			data.append(row[0:(len(row)-1)])
			labels.append(row[len(row)-1])

	f.close()

	return data, labels


def getInputDataFromFile(filePath):
	if '.arff' in filePath:
		return getDataFromArffFile(filePath)
	elif '.txt' in filePath:
		return getDataFromTxtFile(filePath)
	else:
		raise Exception('Tipo de arquivo invalido!')