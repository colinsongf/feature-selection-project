class ResultadoClassificacao(object):
	fileName = ""
	resultados = None

	def __init__(self, fileName, resultados):
		self.fileName = fileName
		self.resultados = resultados

	def getFilename(self):
		return self.fileName

	def getResultados(self):
		return self.resultados