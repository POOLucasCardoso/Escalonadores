import unittest
from Escalonadores import Escalonador,EscalonadorV2
from Processo import Processo

def ticks(vezes,escalonador):
	for i in range(vezes):
		escalonador.escalonar()

class EscalonadorIterativoTeste(unittest.TestCase):

	def estado(self, escalonador, ativos, bloqueados, tick, quantun):
		resultados = str(escalonador)
		esperado = f'''Processos ativos: {ativos}
Processos bloqueados: {bloqueados}
Tick atual: {tick}
Quantun: {quantun}
'''
		self.assertEqual(resultados, esperado)

	def test1(self):
		escalonador = Escalonador()
		self.estado(escalonador, [], [], 0, 3)

	def test2(self):
		escalonador = Escalonador()
		try:
			ticks(1,escalonador)
			self.estado(escalonador, [], [], 1, 3)
		except Exception as e:
			self.fail(str(e))

	def test3(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		self.estado(escalonador, ['Status p1: None'], [], 0, 3)
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 1, 3)
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 2, 3)

	def test4(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 3, 3)

	def test5(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 3, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 6, 3)

	def test6(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		escalonador.addProcesso(Processo('p3'))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p3: w', 'Status p1: r'], [], 3, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p3: w', 'Status p1: w', 'Status p2: r'], [], 6, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: w', 'Status p3: r'], [], 9, 3)

	def test7(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		self.estado(escalonador, ['Status p1: None'], [], 0, 3)
		ticks(3,escalonador)
		escalonador.addProcesso(Processo('p2'))
		self.estado(escalonador, ['Status p1: r', 'Status p2: None'], [], 3, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 6, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 9, 3)
		self.assertEqual(escalonador.pesquisarProcesso('p2').getEstados(),'wwwrrr')

	def test8(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		ticks(1,escalonador)
		escalonador.finalizarProcesso('p1')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p2: r'], [], 2, 3)
		self.assertEqual(escalonador.pesquisarProcesso('p2').getEstados(),'wr')

	def test9(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		ticks(1,escalonador)
		escalonador.finalizarProcesso('p2')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 2, 3)
		ticks(1,escalonador)
		self.assertEqual(escalonador.pesquisarProcesso('p1').getEstados(),'rrr')

	def test10(self):
		escalonador = Escalonador(5)
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		ticks(5,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 5, 5)
		self.assertEqual('|p1|p1|p1|p1|p1|',escalonador.getHistorico())
		ticks(5,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 10, 5)
		self.assertEqual('|p1|p1|p1|p1|p1|p2|p2|p2|p2|p2|',escalonador.getHistorico())

	def test11(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		ticks(2,escalonador)
		escalonador.finalizarProcesso('p1')
		ticks(2,escalonador)
		escalonador.addProcesso(Processo('p2'))
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p2: r'], [], 6, 3)
		self.assertEqual('|p1|p1|None|None|p2|p2|',escalonador.getHistorico())

	def test12(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		escalonador.addProcesso(Processo('p3'))
		ticks(2,escalonador)
		escalonador.bloquearProcesso()
		ticks(4,escalonador)
		self.estado(escalonador, ['Status p3: r', 'Status p2: w'], ['Status p1: b'], 6, 3)
		self.assertEqual('|p1|p1|p2|p2|p2|p3|',escalonador.getHistorico())

	def test13(self):
		escalonador = Escalonador()
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		escalonador.addProcesso(Processo('p3'))
		ticks(2,escalonador)
		escalonador.bloquearProcesso()
		ticks(2,escalonador)
		escalonador.desbloquearProcesso('p1')
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p3: r', 'Status p1: w', 'Status p2: w'], [], 6, 3)
		self.assertEqual('|p1|p1|p2|p2|p2|p3|',escalonador.getHistorico())

	def test14(self):
		escalonador = Escalonador(1)
		escalonador.addProcesso(Processo('p1'))
		escalonador.addProcesso(Processo('p2'))
		escalonador.addProcesso(Processo('p3'))
		escalonador.bloquearProcesso()
		escalonador.bloquearProcesso()
		escalonador.bloquearProcesso()
		ticks(1,escalonador)
		escalonador.desbloquearProcesso('p2')
		escalonador.desbloquearProcesso('p1')
		escalonador.desbloquearProcesso('p3')
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: w', 'Status p3: r'], [], 4, 1)
		self.assertEqual('|None|p2|p1|p3|',escalonador.getHistorico())

	def test15(self):
		escalonador = EscalonadorV2()
		try:
			escalonador.addProcesso(Processo('p1'))
			self.fail("Exceção esperada")
		except Exception as e:
			self.estado(escalonador, [], [], 0, 3)
			self.assertEqual('|',escalonador.getHistorico())

	def test16(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		self.estado(escalonador, ['Status p1: None'], [], 0, 3)
		self.assertEqual('|',escalonador.getHistorico())

	def test17(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.finalizarProcesso('p1')
		self.estado(escalonador, [], [], 0, 3)
		self.assertEqual('|',escalonador.getHistorico())

	def test18(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 3, 3)
		self.assertEqual('|p1|p1|p1|',escalonador.getHistorico())
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 6, 3)
		self.assertEqual('|p1|p1|p1|p2|p2|p2|',escalonador.getHistorico())

	def test19(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		escalonador.addProcesso(Processo('p3',1))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p3: w', 'Status p1: r'], [], 3, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p3: w', 'Status p1: w', 'Status p2: r'], [], 6, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: w', 'Status p3: r'], [], 9, 3)

	def test20(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		self.estado(escalonador, ['Status p1: None'], [], 0, 3)
		ticks(3,escalonador)
		escalonador.addProcesso(Processo('p2',1))
		self.estado(escalonador, ['Status p1: r', 'Status p2: None'], [], 3, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 6, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 9, 3)
		self.assertEqual(escalonador.pesquisarProcesso('p2').getEstados(),'wwwrrr')

	def test21(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		ticks(1,escalonador)
		escalonador.finalizarProcesso('p1')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p2: r'], [], 2, 3)
		self.assertEqual(escalonador.pesquisarProcesso('p2').getEstados(),'wr')

	def test22(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		ticks(1,escalonador)
		escalonador.finalizarProcesso('p2')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 2, 3)
		ticks(1,escalonador)
		self.assertEqual(escalonador.pesquisarProcesso('p1').getEstados(),'rrr')

	def test23(self):
		escalonador = EscalonadorV2(5)
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		ticks(5,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: r'], [], 5, 5)
		self.assertEqual('|p1|p1|p1|p1|p1|',escalonador.getHistorico())
		ticks(5,escalonador)
		self.estado(escalonador, ['Status p1: w', 'Status p2: r'], [], 10, 5)
		self.assertEqual('|p1|p1|p1|p1|p1|p2|p2|p2|p2|p2|',escalonador.getHistorico())

	def test24(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		ticks(2,escalonador)
		escalonador.finalizarProcesso('p1')
		ticks(2,escalonador)
		escalonador.addProcesso(Processo('p2',1))
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p2: r'], [], 6, 3)
		self.assertEqual('|p1|p1|None|None|p2|p2|',escalonador.getHistorico())

	def test25(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		escalonador.addProcesso(Processo('p3',1))
		ticks(2,escalonador)
		escalonador.bloquearProcesso()
		ticks(4,escalonador)
		self.estado(escalonador, ['Status p3: r', 'Status p2: w'], ['Status p1: b'], 6, 3)
		self.assertEqual('|p1|p1|p2|p2|p2|p3|',escalonador.getHistorico())

	def test26(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		escalonador.addProcesso(Processo('p3',1))
		ticks(2,escalonador)
		escalonador.bloquearProcesso()
		ticks(2,escalonador)
		escalonador.desbloquearProcesso('p1')
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p3: r', 'Status p1: w', 'Status p2: w'], [], 6, 3)
		self.assertEqual('|p1|p1|p2|p2|p2|p3|',escalonador.getHistorico())

	def test27(self):
		escalonador = EscalonadorV2(1)
		escalonador.addProcesso(Processo('p1',1))
		escalonador.addProcesso(Processo('p2',1))
		escalonador.addProcesso(Processo('p3',1))
		escalonador.bloquearProcesso()
		escalonador.bloquearProcesso()
		escalonador.bloquearProcesso()
		ticks(1,escalonador)
		escalonador.desbloquearProcesso('p2')
		escalonador.desbloquearProcesso('p1')
		escalonador.desbloquearProcesso('p3')
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: w', 'Status p1: w', 'Status p3: r'], [], 4, 1)
		self.assertEqual('|None|p2|p1|p3|',escalonador.getHistorico())

	def test28(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		ticks(10,escalonador)
		escalonador.addProcesso(Processo('p2',2))
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: r', 'Status p1: w'], [], 13, 3)

	def test29(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',2))
		ticks(10,escalonador)
		escalonador.addProcesso(Processo('p2',1))
		ticks(3,escalonador)
		escalonador.bloquearProcesso()
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p2: r'], ['Status p1: b'], 16, 3)

	def test30(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',2))
		ticks(10,escalonador)
		escalonador.addProcesso(Processo('p2',1))
		ticks(3,escalonador)
		escalonador.bloquearProcesso()
		ticks(3,escalonador)
		escalonador.desbloquearProcesso('p1')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r', 'Status p2: w'], [], 17, 3)

	def test31(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',1))
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 1, 3)
		escalonador.addProcesso(Processo('p2',2))
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p2: r', 'Status p1: w'], [], 2, 3)
		escalonador.finalizarProcesso('p2')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 3, 3)

	def test33(self):
		escalonador = Escalonador()
		try:
			escalonador.addProcesso(Processo('p1',3))
			self.fail('Exceção esperada')
		except Exception:
			self.estado(escalonador, [], [], 0, 3)
			self.assertEqual('|',escalonador.getHistorico())

	def test32(self):
		escalonador = EscalonadorV2()
		escalonador.addProcesso(Processo('p1',2))
		self.estado(escalonador, ['Status p1: None'], [], 0, 3)
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p1: r'], [], 2, 3)
		escalonador.addProcesso(Processo('p2',4))
		ticks(1,escalonador)
		escalonador.bloquearProcesso()
		self.estado(escalonador, ['Status p1: w'], ['Status p2: r'], 3, 3)
		ticks(2,escalonador)
		escalonador.addProcesso(Processo('p3',1))
		self.estado(escalonador, ['Status p1: r', 'Status p3: None'], ['Status p2: b'], 5, 3)
		ticks(1,escalonador)
		escalonador.bloquearProcesso()
		self.estado(escalonador, ['Status p3: w'], ['Status p2: b', 'Status p1: r'], 6, 3)
		ticks(1,escalonador)
		escalonador.desbloquearProcesso('p2')
		self.estado(escalonador, ['Status p2: b', 'Status p3: r'], ['Status p1: b'], 7, 3)
		ticks(1,escalonador)
		escalonador.desbloquearProcesso('p1')
		escalonador.addProcesso(Processo('p4',4))
		self.estado(escalonador, ['Status p2: r', 'Status p4: None', 'Status p1: b', 'Status p3: w'], [], 8, 3)
		ticks(2,escalonador)
		escalonador.addProcesso(Processo('p5',3))
		escalonador.addProcesso(Processo('p6',3))
		ticks(10,escalonador)
		self.estado(escalonador, ['Status p2: r', 'Status p4: w', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 20, 3)
		escalonador.bloquearProcesso()
		ticks(4,escalonador)
		self.estado(escalonador, ['Status p4: r', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], ['Status p2: b'], 24, 3)
		escalonador.desbloquearProcesso('p2')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p4: r', 'Status p2: w', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 25, 3)
		ticks(5,escalonador)
		self.estado(escalonador, ['Status p4: r', 'Status p2: w', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 30, 3)
		escalonador.finalizarProcesso('p4')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p2: r', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 31, 3)
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p2: r', 'Status p5: w', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 32, 3)
		escalonador.finalizarProcesso('p2')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p5: r', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 33, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p6: r', 'Status p5: w', 'Status p1: w', 'Status p3: w'], [], 36, 3)
		ticks(3,escalonador)
		self.estado(escalonador, ['Status p5: r', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 39, 3)
		escalonador.bloquearProcesso()
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p6: r', 'Status p1: w', 'Status p3: w'], ['Status p5: b'], 40, 3)
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p6: r', 'Status p1: w', 'Status p3: w'], ['Status p5: b'], 41, 3)
		ticks(2,escalonador)
		self.estado(escalonador, ['Status p6: r', 'Status p1: w', 'Status p3: w'], ['Status p5: b'], 43, 3)
		ticks(1,escalonador)
		escalonador.desbloquearProcesso('p5')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p5: w', 'Status p6: r', 'Status p1: w', 'Status p3: w'], [], 45, 3)
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p5: r', 'Status p6: w', 'Status p1: w', 'Status p3: w'], [], 46, 3)
		escalonador.finalizarProcesso('p6')
		ticks(1,escalonador)
		self.estado(escalonador, ['Status p5: r', 'Status p1: w', 'Status p3: w'], [], 47, 3)

########################################################
if __name__ == '__main__':
	
	unittest.main()
