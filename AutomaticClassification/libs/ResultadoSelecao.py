class ResultadoSelecao(object):
	filePath	 = None
	sample 		 = None
	comparison 	 = None
	fileUsed 	 = None
	resultadoSelecao = None

	def __init__(self, filePath, sample, comparison, fileUsed, resultadoSelecao):
		self.filePath = filePath
		self.sample = sample
		self.comparison = comparison
		self.fileUsed = fileUsed
		self.resultadoSelecao = resultadoSelecao

	def getFilePath(self):
		return self.filePath

	def getSample(self):
		return self.sample

	def getComparison(self):
		return self.comparison

	def getFileUsed(self):
		return self.fileUsed

	def getResultadoSelecao(self):
		return self.resultadoSelecao