from Erros import *
from Fila import FilaPrioridade as Fila
from Processo import Processo

class Escalonador(object):

	def __init__(self, quantun=3):
		self.quantun = quantun
		self.processosAtivos = []
		self.processosIO = []
		self.historico = []
		self.processo = None
		self.fila = Fila()
		self.tick = 0

	def addProcesso(self, id, prioridade):
		processo = Processo(id, len(self.historico), prioridade)
		self.fila.enfileirar(processo)
		self.processosAtivos.append(processo)
		if self.processo == None:
			self.processo = self.fila.desenfileirar()
		elif self.processo.prioridade < prioridade:
			self.fila.reenfileirar(self.processo)
			self.tick = 0
			self.processo = self.fila.desenfileirar()

	def pesquisarProcesso(self, id):
		for p in (self.processosAtivos+self.processosIO):
			if p.nome == id:
				return p
		raise ProcessoInexistenteException('Nenhum processo encontrado com o ID informado')

	def getHistorico(self):
		retorno = '|'
		for s in self.historico:
			retorno+=s+'|'
		return retorno

	def finalizarProcesso(self, processo):
		if processo.__class__ is str:
			try:
				processo = self.pesquisarProcesso(processo)
			except ProcessoInexistenteException as PIe:
				raise PIe
		self.processosAtivos.remove(processo)
		if processo == self.processo:
			self.tick = 0
			try:
				self.processo = self.fila.desenfileirar()
			except FilaVaziaException:
				self.processo = None
		else:
			try:
				self.fila.remover(processo)
			except ProcessoInexistenteException:
				self.processo = None

	def definirEstado(self, processo):
		if processo == self.processo:
			processo.addEstado('r')
		else:
			processo.addEstado('w')

	def escalonar(self):
		try:
			for p in self.processosAtivos:
				self.definirEstado(p)
			for p in self.processosIO:
				p.addEstado('b')

			if self.processo != None:
				self.tick+=1
				self.historico.append(self.processo.nome)
				if self.tick == self.quantun:
					self.fila.reenfileirar(self.processo)
					self.tick = 0
					self.processo = self.fila.desenfileirar()
			else:
				self.historico.append('None')
				self.processo = self.fila.desenfileirar()
		except FilaVaziaException:
			self.tick = 0
			self.processo = None

	def __str__(self):
		ativos = f'Processos ativos: {list(map(str,self.processosAtivos))}\n'
		bloqueados = f'Processos bloqueados: {list(map(str,self.processosIO))}\n'
		tick = f'Tick atual: {len(self.historico)}\n'
		quantun = f'Quantun: {self.quantun}\n'
		processo = f'Processo rodando'
		historico = f'Histórico: {self.getHistorico()}'
		return ativos+bloqueados+tick+quantun+historico

	def bloquearProcesso(self):
		self.processosAtivos.remove(self.processo)
		self.processosIO.append(self.processo)
		self.tick = 0
		try:
			self.processo = self.fila.desenfileirar()
		except FilaVaziaException:
			self.processo = None

	def desbloquearProcesso(self, processo):
		if processo.__class__ is str:
			try:
				processo = self.pesquisarProcesso(processo)
			except ProcessoInexistenteException as PIe:
				raise PIe
		if not processo.isBloked():
			raise OperacaoInvalidaException('O processo informado não está bloqueado.')
		self.processosAtivos.append(processo)
		self.processosIO.remove(processo)
		self.fila.reenfileirar(processo)
		if self.processo == None:
			self.processo = self.fila.desenfileirar()
		elif self.processo.prioridade < processo.prioridade:
			self.fila.reenfileirar(self.processo)
			self.tick = 0
			self.processo = self.fila.desenfileirar()
