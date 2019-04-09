class FilaVaziaException(Exception):
	def __init__(self, msg):
		self.message = msg

class ProcessoInexistenteException(Exception):
	def __init__(self, msg):
		self.message = msg

class OperacaoInvalidaException(Exception):
	def __init__(self, msg):
		self.message = msg
