import numpy as np

def getSortedIndexes(array):
		return getBestIndexes(array.size)


def getBestIndexes(array, n):
	if(not array.any()):
		raise Exception('Empty array!')
	
	sortedIndexes = np.argsort(array)
	size = len(sortedIndexes)

	if(n < 0 or n > size):
		raise Exception('Invalid number of best N indexes!')

	if(n != 0):
		bestNIndexes = []
		for i in range((size - 1), (size - 1 - n), -1):
			bestNIndexes.append(sortedIndexes[i])
		return bestNIndexes
	else:
		return sortedIndexes


def getColumns2DList(listToFilter, columns):
	newList = []

	for row in listToFilter:
		newRow = []

		for index in columns:
			newRow.append(row[index])

		newList.append(newRow)

	return newList