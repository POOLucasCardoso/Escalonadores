from Erros import FilaVaziaException,ProcessoInexistenteException

class Fila(object):

	def __init__(self):
		self.fila = []

	def enfileirar(self, obj):
		self.fila.insert(0, obj)

	def desenfileirar(self):
		try:
			return self.fila.pop(0)
		except IndexError:
			raise FilaVaziaException('Fila vazia')

	def reenfileirar(self, obj):
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

	def enfileirar(self, obj):
		#print('enfileirando em:',list(map(str,self.fila)))
		if not len(self.fila):
			self.fila.append(obj)
		else:
			for i in range(len(self.fila)):
				if self.fila[i].prioridade <= obj.prioridade:
					self.fila.insert(i,obj)
					break

	def desenfileirar(self): #raises FilaVaziaException;
		#print('desenfileirando em:',list(map(str,self.fila)))
		#for i in self.fila:
		#	if len(i.estados)>6:
		#		i.prioUp(1)
		#self.fila = mergeSort(self.fila)
		try:
			return self.fila.pop(0)
		except IndexError:
			raise FilaVaziaException('Fila vazia')

	def reenfileirar(self, obj):
		#print('reenfileirando em:',list(map(str,self.fila)))
		if not len(self.fila):
			self.fila.append(obj)
		else:
			for i in range(len(self.fila)):
				if self.fila[i].prioridade < obj.prioridade:
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
