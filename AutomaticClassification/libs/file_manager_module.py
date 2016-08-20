import os
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
	f = open(filePath)
	
	labels = []
	data = []
	
	for line in f:
		row = line.split(' ')
		for c in row:
			if c == '\n':
				row.remove(c)
				
		data.append(row[0:(len(row)-1)])
		labels.append(row[len(row)-1])
		
	return data, labels


def getDataFromArffFile(filePath):
	f = open(filePath)

	inData = False

	labels = []
	data = []
	
	for line in f:
		if('@data' in line):
			inData = True
			continue

		if(inData == True and line != '\n'):
			row = line.split(' ')
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