package roundRobin;

import java.util.LinkedList;

public class Escalonador extends Object{
	
	private LinkedList<Processo> processos;
	private int quantun;
	private LinkedList<String>historico;
	
	public Escalonador(int quantun) {
		super();
		this.quantun = quantun;
		processos = new LinkedList<Processo>();
		historico = new LinkedList<String>();
	}

	public int getQuantun() {
		return quantun;
	}

	public void setQuantun(int quantun) {
		this.quantun = quantun;
	}

	public Processo[] getFilaDeProcessos() {
		Processo[] retorno = new Processo[processos.size()];
		retorno = processos.toArray(retorno);
		return retorno;
	}
	
	public void addProcesso(Processo p) {
		if (processos.size()==0) {
			processos.add(p);
		}else {
			for(int i = 0; i <processos.size(); i++) {
				if(p.getMomento()<processos.get(i).getMomento()) {
					processos.add(i, p);
					break;
				}
			}if(!processos.contains(p)) {
				processos.add(p);
			}
		}
	}
	
	public String pesquisarProcesso(String id) throws ProcessoInexistenteException {
		String retorno = new String();
		for(Processo p: processos) {
			if(p.getNome()==id) {
				for(String estado:p.getEstados()) {
					retorno+=estado;
				}
				return retorno;
			}
		}
		throw new ProcessoInexistenteException("Nenhum processo encontrado com o ID informado");
	}
	
	public String getHistoricoDeProcessos() {
		String retorno = new String();
		for(String processo:historico) {
			retorno+="|"+processo;
		}
		return retorno;
	}
	
	public void escalonar() {
		Fila fila = new Fila();
		Processo processo = null;
		int cont = 0;
		while(continuar()) {
			try {
				for(Processo p: this.processos) {
					if(p.getMomento()==historico.size()) {
						fila.enfileirar(p);
						try {
							if(processo==null) {
								processo = fila.desenfileirar();
							}
						} catch (FilaVaziaException e1) {
							throw e1;
						}
					}if(p == processo) {
						p.addEstado("r");
					}else if(!fila.conteins(p)&&(!p.isOver())) {
						p.addEstado("i");
					}else if(!p.isOver()) {
						p.addEstado("w");
					}
					
				}
				if(processo!=null) {
					cont+=1;
					processo.setQuantun(processo.getQuantun()-1);
					historico.add(processo.getNome());
					if(processo.getQuantun()==0) {
						processo.addEstado("f");
						cont=0;
						processo = fila.desenfileirar();
					}else if(cont==quantun){
						fila.reenfileirar(processo);
						processo = fila.desenfileirar();
						cont=0;
					}
				}else {
					historico.add("Null");
				}
			}catch(FilaVaziaException fle) {
				cont = 0;
				processo = null;
			}
		}
	}
	private boolean continuar() {
		for(Processo p: processos) {
			if(!p.isOver()) {
				return true;
			}
		}
		return false;
	}
	
	public String toString() {
		String retorno = "";
		for(Processo p: this.getFilaDeProcessos()) {
			retorno += p+"\n";
		}
		retorno += "Histórico: "+getHistoricoDeProcessos();
		return retorno;
	}
}
