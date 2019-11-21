# Caixeiro Viajante Assimétrico
Resolução do problema do Caixeiro Viajante utilizando o algoritmo Clark-Wright e 3-opt para a disciplina de Algoritmo em Grafos do Programa de Pós Graduação da Universidade Estadual de Maringá (UEM)

## Team:
* [Simone França](https://github.com/simonefranca)
* [Marco Aurélio Paulino](https://github.com/marcoADP)

## Execução:
Precisa ter o Python 3 instalado em seu computador

Para executar, acesse a pasta em que está o caixeiro_viajante.py pelo terminal a sua escolha.

Digite o seguinte comando para executar a instância ft53:
	python caixeiro_viajante.py ft53.atsp
	
Caso a instância não esteja na mesma pasta que o caixeiro_viajante.py é necessário digitar o caminho até o arquivo.
	python caixeiro_viajante.py instancia/ft53.atsp	- Caso a pasta instancia esteja junto ao .py
	ou
	python caixeiro_viajante.py e:/Projetos/caixeiro_viajante/instancias/ft53.atsp - Caminho completo até a instância
	

Note que não é necessário colocar qualquer tipo de aspas no comando

Caso queira executar a partir de uma IDE, comente as linhas:

if __name__ == "__main__":
    main(sys.argv[1])
	
E só chamar a função main, em que o parâmetro file é a instância de teste, neste caso precisa de aspas.
	main(file='ft53.atsp')
	
