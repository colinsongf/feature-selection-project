from ... import definitions
import numpy as np
from sklearn import tree, linear_model, svm
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from libs.FeatureSelectionMethods.T_Statistics import T_Statistics
from individual.Individual import Individual

def generateIndividual(numberOfFeatures):
	# Estrutura genética:
	# Gene[0] -> espaço reservado para armazenar o caminho do arquivo utilizado posteriormente
	# Gene[1] -> int [0, numberOfFeatureSelectionMethods): representa o método de seleção a ser utilizado nesse indivíduo
	# Gene[2] -> int [1, numberOfFeatures]: número de atributos a serem selecionados. Se maior que o número disponível, raise Exception
	# Gene[3] -> int [0, numberOfClassificationMethods): representa o método de classificação a ser utilizado nesse indivíduo
	newGene = []

	# Deixa o espaço do arquivo livre
	newGene.append(None)
	
	# Método de seleção
	newGene.append( np.random.randint(0, len(definitions.selectors)) )

	# Número de características a serem selecionadas
	newGene.append( np.random.randint(1, numberOfFeatures + 1) )
	
	# Método de classificação
	newGene.append( np.random.randint(0, len(definitions.classifier)) )

	return Individual(newGene)