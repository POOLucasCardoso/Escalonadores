from Erros import *
from Fila import Fila,FilaPrioridade
from Processo import Processo

class EscalonadorAbstrato(object):

	def __init__(self, quantun):
		self.quantun = quantun
		self.processosIO = []
		self.historico = []
		self.processo = None
		self.tick = 0

	def pesquisarProcesso(self, id): #raises: ProcessoInexistenteException;
		listaProcessos = self.fila.fila+self.processosIO+[self.processo]
		for p in (listaProcessos):
			if p.nome == id:
				return p
		raise ProcessoInexistenteException(f'Nenhum processo encontrado com o ID {id}')

	def getHistorico(self):
		retorno = '|'
		for s in self.historico:
			retorno+=s+'|'
		return retorno

	def finalizarProcesso(self, id): #raises: ProcessoInexistenteException;
		try:
			processo = self.pesquisarProcesso(id)
		except ProcessoInexistenteException as PIe:
			raise PIe
		try:
			if processo == self.processo:
				self.tick = 0
				self.processo = self.fila.desenfileirar()
			else:
				self.fila.remover(processo)
		except FilaVaziaException:
				self.processo = None
		except ProcessoInexistenteException:
				self.processo = None

	def escalonar(self):
		try:
			for p in self.fila.fila:
				p.addEstado('w')
			for p in self.processosIO:
				p.addEstado('b')

			if self.processo == None:
				self.historico.append('None')
				self.processo = self.fila.desenfileirar()
			else:
				self.processo.addEstado('r')
				self.tick+=1
				self.historico.append(self.processo.nome)
				if self.tick == self.quantun:
					self.tick = 0
					self.fila.enfileirar(self.processo)
					self.processo = self.fila.desenfileirar()
		except FilaVaziaException:
			self.tick = 0
			self.processo = None

	def bloquearProcesso(self):
		self.processosIO.append(self.processo)
		self.tick = 0
		try:
			self.processo = self.fila.desenfileirar()
		except FilaVaziaException:
			self.processo = None

	def desbloquearProcesso(self, id): #raises OperacaoInvalidaException;
		try:
			processo = self.pesquisarProcesso(id)
		except ProcessoInexistenteException as PIe:
			raise PIe
		if not processo.isBloked():
			raise OperacaoInvalidaException('O processo informado não está bloqueado.')
		self.processosIO.remove(processo)
		self.addProcesso(processo)

	def __str__(self):
		if self.processo == None:
			ativos = f'Processos ativos: {list(map(str,self.fila.fila))}\n'
		else:
			ativos = f'Processos ativos: {list(map(str,[self.processo]+self.fila.fila))}\n'
		bloqueados = f'Processos bloqueados: {list(map(str,self.processosIO))}\n'
		tick = f'Tick atual: {len(self.historico)}\n'
		quantun = f'Quantun: {self.quantun}\n'
		return ativos+bloqueados+tick+quantun

class Escalonador(EscalonadorAbstrato):

	def __init__(self, quantun=3):
		super().__init__(quantun)
		self.fila = Fila()

	def addProcesso(self, processo):
		if processo.prioridade != 0:
			raise OperacaoInvalidaException('O processo não poderia possuir prioridade.')
		self.fila.enfileirar(processo)
		if self.processo == None:
			self.processo = self.fila.desenfileirar()

class EscalonadorV2(EscalonadorAbstrato):

	def __init__(self, quantun=3):
		super().__init__(quantun)
		self.fila = FilaPrioridade()

	def addProcesso(self, processo): #raises OperacaoInvalidaException;
		if processo.prioridade == 0:
			raise OperacaoInvalidaException('O processo deve ter prioridade de mo mínimo 1')
		self.fila.enfileirar(processo)
		if self.processo == None:
			self.processo = self.fila.desenfileirar()
		elif self.processo.prioridade < processo.prioridade:
			self.fila.enfileirar(self.processo)
			self.tick = 0
			self.processo = self.fila.desenfileirar()
