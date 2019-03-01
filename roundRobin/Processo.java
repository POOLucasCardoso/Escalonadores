package roundRobin;

import java.util.LinkedList;
import java.util.NoSuchElementException;

public class Processo extends Object {
	
	private String nome;
	private int momento;
	private int quantun;
	private LinkedList<String> estados;
	
	public Processo(String nome, int momento, int quantun) {
		super();
		this.nome = nome;
		this.momento = momento;
		this.quantun = quantun;
		estados = new LinkedList<String>();
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public int getMomento() {
		return momento;
	}

	public void setMomento(int momento) {
		this.momento = momento;
	}

	public int getQuantun() {
		return quantun;
	}

	public void setQuantun(int quantun) {
		this.quantun = quantun;
	}

	public String[] getEstados() {
		return estados.toArray(new String[1]);
	}

	public void addEstado(String estado) {
		this.estados.add(estado);
	}
	
	public boolean isOver() {
		try {
			if(estados.getLast()=="f") {
				return true;
			}
		} catch (NoSuchElementException e) {
			return false;
		}
		return false;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((nome == null) ? 0 : nome.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Processo other = (Processo) obj;
		if (nome == null) {
			if (other.nome != null)
				return false;
		} else if (!nome.equals(other.nome))
			return false;
		return true;
	}
	
	public String toString() {
		return nome+"|"+momento+"|"+quantun;
	}

}
