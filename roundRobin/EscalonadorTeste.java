package roundRobin;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class EscalonadorTeste {
	
	@Test
	void teste_padrao() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",0,4));
		
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrrrf");
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}

	@Test
	void teste_processador_ocioso_no_inicio() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",3,4));
		
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"iiirrrrf");
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste_com_dois_processos() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",0,4));
		processador.addProcesso(new Processo("2",0,3));
		
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrrwwwrf");
			assertEquals(processador.pesquisarProcesso("2"),"wwwrrrf");
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste_com_diferentes_momentos() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",0,4));
		processador.addProcesso(new Processo("2",2,3));
		processador.escalonar();
		System.out.println(processador);
		try {
			System.out.println(processador.pesquisarProcesso("2"));
			assertEquals(processador.pesquisarProcesso("1"),"rrrwwwrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiwrrrf");
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste_de_ociosidade_no_meio() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",0,2));
		processador.addProcesso(new Processo("2",4,3));
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiiirrrf");
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste_com_tres_processos() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",0,4));
		processador.addProcesso(new Processo("2",2,3));
		processador.addProcesso(new Processo("3",4,5));
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrrwwwwwwrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiwrrrf");
			assertEquals(processador.pesquisarProcesso("3"),"iiiiwwrrrwrrf");
			
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste7() {
		Escalonador processador = new Escalonador(3);
		processador.addProcesso(new Processo("1",2,7));
		processador.addProcesso(new Processo("2",5,3));
		processador.addProcesso(new Processo("3",1,6));
		processador.addProcesso(new Processo("4",3,6));
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"iiwwwwwwwwrrrwwwwwwrrrrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiiiiwwrrrf");
			assertEquals(processador.pesquisarProcesso("3"),"irrrwwwwwwwwwrrrf");
			assertEquals(processador.pesquisarProcesso("4"),"iiiwrrrwwwwwwwwwrrrf");
			
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
		
	}
	
	@Test
	void teste8() {
		Escalonador processador = new Escalonador(3);
		
		processador.addProcesso(new Processo("1",1,8));
		processador.addProcesso(new Processo("2",5,5));
		processador.addProcesso(new Processo("3",4,2));
		processador.escalonar();
		System.out.println(processador);
		try {
			assertEquals(processador.pesquisarProcesso("1"),"irrrrrrwwwwwrrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiiiiwwrrrwwwwrrf");
			assertEquals(processador.pesquisarProcesso("3"),"iiiiwwwwwwrrf");
			
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}
	}
	
	@Test
	void teste_quantun_4() {
		Escalonador processador = new Escalonador(4);
		
		processador.addProcesso(new Processo("1",0,3));
		processador.addProcesso(new Processo("2",2,8));
		processador.addProcesso(new Processo("3",4,2));
		processador.addProcesso(new Processo("4",2,5));
		processador.addProcesso(new Processo("5",5,3));
		processador.escalonar();
		System.out.println(processador);
		
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiwwwwwwwwwwrrrrwrrrrf");
			assertEquals(processador.pesquisarProcesso("3"),"iiiiwwwwwwrrf");
			assertEquals(processador.pesquisarProcesso("4"),"iiwrrrrwwwwwwwwwrf");
			assertEquals(processador.pesquisarProcesso("5"),"iiiiiwwrrrf");
			
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}

	}
	
	@Test
	void teste_quantun_5() {
		Escalonador processador = new Escalonador(5);
		
		processador.addProcesso(new Processo("1",0,3));
		processador.addProcesso(new Processo("2",2,8));
		processador.addProcesso(new Processo("3",4,2));
		processador.addProcesso(new Processo("4",2,5));
		processador.addProcesso(new Processo("5",5,3));
		processador.escalonar();
		System.out.println(processador);
		
		try {
			assertEquals(processador.pesquisarProcesso("1"),"rrrf");
			assertEquals(processador.pesquisarProcesso("2"),"iiwwwwwwwwwwwrrrrrrrrf");
			assertEquals(processador.pesquisarProcesso("3"),"iiiiwwwwwwwrrf");
			assertEquals(processador.pesquisarProcesso("4"),"iiwrrrrrf");
			assertEquals(processador.pesquisarProcesso("5"),"iiiiiwwwrrrf");
			
		} catch (ProcessoInexistenteException pie) {
			System.out.println(pie.getMessage());
			fail(pie.getMessage());
		}

	}

}
