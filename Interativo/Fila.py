from Erros import FilaVaziaException,ProcessoInexistenteException

class Fila(object):

	def __init__(self):
		self.fila = []

	def desenfileirar(self):
		try:
			return self.fila.pop(0)
		except IndexError:
			raise FilaVaziaException('Fila vazia')

	def enfileirar(self, obj):
		self.fila.append(obj)

	def remover(self, obj):
		try:
			self.fila.remove(obj)
		except ValueError:
			raise ProcessoInexistenteException('Processo não está enfileirado.')

	def conteins(self, obj):
		return obj in self.fila

class FilaPrioridade(object):

	def __init__(self):
			self.fila = []

	def desenfileirar(self): #raises FilaVaziaException;
		try:
			return self.fila.pop(0)
		except IndexError:
			raise FilaVaziaException('Fila vazia')

	def enfileirar(self, obj):
		if len(self.fila) == 0:
			self.fila.append(obj)
		else:
			for i in range(len(self.fila)):
				if obj.prioridade > self.fila[i].prioridade:
					self.fila.insert(i,obj)
					break
		if not self.conteins(obj):
			self.fila.append(obj)
	def remover(self, obj):
		try:
			self.fila.remove(obj)
		except ValueError:
			raise ProcessoInexistenteException('Processo não está enfileirado.')

	def conteins(self, obj):
		return obj in self.fila
