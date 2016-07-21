class Classificador(object):
	name = ""
	wekaClassifier = ""

	def __init__(self, name, wekaClassifier):
		self.name = name
		self.wekaClassifier = wekaClassifier


class ResultadoClassificacao(object):
	fileName = ""
	resultados = []

	def __init__(self, fileName, resultados):
		self.fileName = fileName
		self.resultados = resultados

	def getFilename(self):
		return self.fileName

	def getResultados(self):
		return self.resultados

class ResultadoSelecao(object):
	sample 		 = None
	comparison 	 = None
	fileUsed 	 = None
	resultadoSelecao = None

	def __init__(self, sample, comparison, fileUsed, resultadoSelecao):
		self.sample = sample
		self.comparison = comparison
		self.fileUsed = fileUsed
		self.resultadoSelecao = resultadoSelecao

	def getSample(self):
		return self.sample

	def getComparison(self):
		return self.comparison

	def getFileUsed(self):
		return self.fileUsed

	def getResultadoSelecao(self):
		return self.resultadoSelecao
