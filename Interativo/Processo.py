class Processo(object):

	def __init__(self, nome, prioridade=0):
		self.nome = nome
		self.estados = []
		self.prioridade = prioridade
		self.prioridadeDef = prioridade

	def addEstado(self, estado):
		self.estados.append(estado)

	def getEstados(self):
		retorno = ''
		for i in self.estados:
			retorno+=i
		return retorno

	def prioUp(self,quant):
		self.prioridade+=quant

	def prioRedef(self):
		self.prioridade = self.prioridadeDef

	def __eq__(self, obj):

		if obj == None:
			return False
		if self.__class__ != obj.__class__:
			return False
		if self.nome == obj.nome:
			return True
		return False

	def __str__(self):
		retorno = 'Status '+self.nome+': '
		try:
			retorno+=self.estados[-1]
		except IndexError:
			retorno+='None'
		return retorno

	def isBloked(self):
		try:
			if self.estados[-1] == 'b':
				return True
		except IndexError:
			return False
		return False
 