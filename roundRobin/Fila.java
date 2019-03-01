package roundRobin;

import java.util.LinkedList;

public class Fila {
	
	LinkedList<Processo> fila = new LinkedList<Processo>();
	
	public void enfileirar(Processo objeto) {
		fila.add(0, objeto);
	}
	
	public Processo desenfileirar() throws FilaVaziaException{
		try {
			Processo retorno = fila.get(0);
			fila.remove(retorno);
			return retorno;
		}catch(Exception e) {
			throw new FilaVaziaException("Fila do processador vazia");
		}
	}
	
	public void reenfileirar(Processo p) {
		fila.add(p);
	}
	
	public boolean conteins(Processo p) {
		return fila.contains(p);
	}

}
