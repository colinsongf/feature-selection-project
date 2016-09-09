import os
import string
import libs.constants as constants
import libs.dicts

selectionResultsFilePath 		= constants.resultsDirPath + '/' + constants.resultsSelectionFileName
classificationResultsFilePath	= constants.resultsDirPath + '/' + constants.resultsClassificationFileName


# METHODS #

def getNumberOfSelectedFeatures():
	f = open(selectionResultsFilePath, 'r')

	selectionLinesRead = []

	rawLines = f.readlines()
	for l in rawLines:
		l = string.strip(l)
		if l:
			selectionLinesRead.append(l)

	f.close()

	splittedLine = string.split(selectionLinesRead[0], ';')

	numSelectedFeatures = len(string.split(splittedLine[len(splittedLine)-1], ','))

	return numSelectedFeatures


def read_classification_results():
