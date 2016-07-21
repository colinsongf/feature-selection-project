import os
import sys
import numpy as np

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
