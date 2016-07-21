# coding=utf-8
import numpy as np

class CapacityAnalysis(object):
	########
	# Attr #
	########
	matrixesToAnalyse	= None
	capacityArray		= None

	###########
	# Methods #
	###########
	def __init__(self, matrixA, matrixB):
		x = np.array(matrixA)
		y = np.array(matrixB)

		(_, cX) = x.shape
		(_, cY) = y.shape

		if(cX != cY):
			raise Exception('Different number of columns from matrixes!')
			
		self.matrixesToAnalyse = [np.array(matrixA), np.array(matrixB)]


	def calculate(self):
		# Pega as dimensões das matrizes dadas com entrada
		(rowsA, colsA) = self.matrixesToAnalyse[0].shape
		(rowsB, colsB) = self.matrixesToAnalyse[1].shape

		# CALCULO DAS MEDIAS DAS MATRIZES
		# Soma todas as linhas de cada coluna
		sumA = np.sum(self.matrixesToAnalyse[0], axis=0)
		sumB = np.sum(self.matrixesToAnalyse[1], axis=0)

		# Calcula os valores médios dados por cada descritor
		mediasA = np.divide(sumA, float(rowsA))
		mediasB = np.divide(sumB, float(rowsB))

		# Calcula a variância de cada descritor (coluna das matrizes)
		varianciaA = np.var(self.matrixesToAnalyse[0], axis=0, ddof=1)
		varianciaB = np.var(self.matrixesToAnalyse[1], axis=0, ddof=1)

		# Cálculo da Análise de Capacidade
		self.capacityArray = np.zeros((colsA))
		for d in range(0, colsA):
			# Parte de cima da fórmula
			up = np.subtract( (mediasA[d]), (mediasB[d]) )

			# Parte de baixo da fórmula
			sqrtLeft = np.divide(varianciaA[d], float(rowsA))
			sqrtRight = np.divide(varianciaB[d], float(rowsB))
			down = np.sqrt( np.add(sqrtLeft, sqrtRight) )

			# Dividindo a parte de cima pela de baixo
			self.capacityArray[d] = np.divide(up, down)

		# Guarda o módulo da capacidade de cada descritor
		self.capacityArray = np.absolute(self.capacityArray)


	def getResult(self):
		return self.capacityArray


	def getSortedIndexes(self):
		return self.getBestIndexes(self.capacityArray.size)


	def getBestIndexes(self, n):
		if(not self.capacityArray.any()):
			raise Exception('The capacity array has not been calculated yet!')
		
		sortedIndexes = np.argsort(self.capacityArray)
		size = sortedIndexes.size

		if(n <= 0 or n > size):
			raise Exception('Invalid number of best N indexes!')

		bestNIndexes = []
		for i in range((size - 1), (size - 1 - n), -1):
			bestNIndexes.append(sortedIndexes[i])

		return bestNIndexes