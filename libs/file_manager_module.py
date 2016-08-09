import os
import sys
import numpy as np
from weka.core.converters import Loader
from natsort import natsorted


def setEncode():
	reload(sys)
	sys.setdefaultencoding('utf8')


def listAllFilesFromPathWithSubstring(path, substring):
	setEncode()
	filePaths = []

	for root, dirs, files in os.walk(path):
		for f in files:
			if substring in f:
				filePaths.append(f)

	return filePaths


def listAllDirFromPath(path):
	setEncode()
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


def getTesteFilesNames(sample, comparison, extension):
	path = dataPath + '/' + sample + '/' + comparison
	files = listAllFilesFromPathWithSubstring(path, extension)

	TesteFiles = []
	for f in files:
		if 'Teste' in f:
			TesteFiles.append(f)

	TesteFiles = natsorted(TesteFiles)
	return TesteFiles


def getMatrixesFromFile(filePath):
	data = np.loadtxt(filePath)

	[rows, columns] = data.shape

	labels = np.unique(data[:, (columns-1)])

	matA = []
	matB = []

	for r in range(0, rows):
		if(data[r, columns-1] == labels[0]):
			matA.append(data[r, 0:(columns-1)])
		elif(data[r, columns-1] == labels[1]):
			matB.append(data[r, 0:(columns-1)])

	matA = np.array(matA)
	matB = np.array(matB)
	return matA, matB


def getMatrixesFromArffFile(filePath):
	f = open(filePath)

	inData = False
	matA = []
	matB = []

	for line in f:
		if ('@attribute' in line) and ('class' in line):
			#print(line)
			classLabels = line.split('{')
			classLabels = classLabels[1].split(',')
			classLabels[1] = classLabels[1][0:(len(classLabels[1])-2)]
			for label in classLabels:
				label = float(label)

		if('@data' in line):
			inData = True
			continue

		if(inData == True and line != '\n'):
			row = line.split(' ')
			for i in row:
				if i == '\n':
					row.remove(i)
				else:
					i = float(i)

			if(row[len(row)-1] == classLabels[0]):
				matA.append(row[0:len(row)-1])
			elif(row[len(row)-1] == classLabels[1]):
				matB.append(row[0:len(row)-1])

	f.close()

	matA = np.array(matA).astype(np.float)
	matB = np.array(matB).astype(np.float)
	return matA, matB