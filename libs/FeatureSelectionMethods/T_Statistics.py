# coding=utf-8
import numpy as np

class T_Statistics(object):
	########
	# Attr #
	########
	matA			= None
	matB			= None
	capacityArray		= None

	###########
	# Methods #
	###########
	def __init__(self, dataInput, labelInput):
		(x, y) = self.assembleMatrixes(dataInput, labelInput)

		(_, cX) = x.shape
		(_, cY) = y.shape

		if(cX != cY):
			raise Exception('Numero diferente de descritores utilizados!')
			
		self.matA = x
		self.matB = y


	def assembleMatrixes(self, dataInput, labelInput):
		matA = []
		matB = []
		uniqueLabels = set(labelInput)
		uniqueLabels = list(uniqueLabels)
		
		if(len(uniqueLabels) > 2):
			raise Exception('Numero de labels maior que 2!')
		
		for i in range(0, len(dataInput)):
			if(labelInput[i] == uniqueLabels[0]):
				matA.append(dataInput[i])
			elif(labelInput[i] == uniqueLabels[1]):
				matB.append(dataInput[i])
				
		matA = np.array(matA).astype(np.float)
		matB = np.array(matB).astype(np.float)
		return matA, matB
	

	def calculate(self):
		# Pega as dimensões das matrizes dadas com entrada
		(rowsA, colsA) 	= self.matA.shape
		(rowsB, _) 		= self.matB.shape

		# CALCULO DAS MEDIAS DAS MATRIZES
		# Soma todas as linhas de cada coluna
		sumA = np.sum(self.matA, axis=0)
		sumB = np.sum(self.matB, axis=0)

		# Calcula os valores médios dados por cada descritor
		mediasA = np.divide(sumA, float(rowsA))
		mediasB = np.divide(sumB, float(rowsB))

		# Calcula a variância de cada descritor (coluna das matrizes)
		varianciaA = np.var(self.matA, axis=0, ddof=1)
		varianciaB = np.var(self.matB, axis=0, ddof=1)

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