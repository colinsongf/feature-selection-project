import os

dataPath                        = '/home/eduardo/Documents/Pos-Graduacao/Trabalho mestrado/Dados/WFS'
resultsDirPath                  = os.getcwd() + '/results'
resultsSelectionFileName        = 'selection.txt'
resultsClassificationFileName   = 'classification.txt'
newFilesPath                    = os.getcwd() + '/newFiles'
resourcesDir                    = os.getcwd() + '/resources'
resTrainingFiles                = resourcesDir + '/trainingFilePaths.txt'
resTestFiles                    = resourcesDir + '/testFilePaths.txt'
fileExtension                   = '.arff'

# Literais
TStatistics = "TStatistics"
DecisionTree = "DecisionTree"
Lasso = "Lasso"
SVM = "SVM"
GaussianNB = "GaussianNaiveBayes"
MultinomialNB = "MultinomialNB"
BernoulliNB = "BernoulliNB"