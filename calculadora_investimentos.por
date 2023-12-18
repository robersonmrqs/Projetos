programa
{   
    	
    	// Calculadora de Investimentos
    	// Criado por Roberson Marques e Bianca Rodrigues
    	// Data: 19/10//2023

    	funcao inicio()
    	{
    
    		// Declaração de variáveis
    
    		inteiro idadeIni, idadeFim, tempo, i
    		real investIni, investPos, capital, juros, montante, calculoExp, calculoExp1
    		cadeia nome, sobrenome
    		caracter periodo

    		// Entrada de dados

    		escreva("Digite o seu nome: ")
    		leia(nome)
		limpa()
		escreva("Digite o seu sobrenome: ")
    		leia(sobrenome)
		limpa()
		escreva("Digite a sua idade: ")
		leia(idadeIni)
		limpa()
		escreva("Digite o valor inicial: R$ ")
    		leia(investIni)
		limpa()
		escreva("Informe valor de investimentos posteriores: R$ ")
    		leia(investPos)
    		limpa()
    		escreva("O investimento será em (m)eses ou (a)nos: ")
    		leia(periodo)
    		limpa()
    		escreva("Informe a quantidade de meses ou anos: ")
    		leia(tempo)
		limpa()
		escreva("Informe o valor da taxa (%): ")
    		leia(juros)
    		limpa()

		// Cálculo

    		juros = juros / 100
    		se(periodo == 'a')
    		{
			tempo = tempo * 12
    		}
		capital = investIni + investPos * tempo
		calculoExp = 0.0
		calculoExp1 = 0.0
   		para(i = 1; i <= tempo; i++)
      	{		
      		se(calculoExp == 0)
      		{
    				calculoExp = 1 + juros
      		}	
      		senao
      		{
      			calculoExp = calculoExp * (1 + juros)
      		}
      	}
      	calculoExp1 = calculoExp - 1
     	se(investIni == 0)
      	{
      		investIni = 1.0
      	}	
     	montante = investIni * calculoExp + investPos * calculoExp1 / juros
		idadeFim = idadeIni + (tempo / 12) 	
	
		// Saída de dados
	
		escreva("\nSeu nome é: ",nome, " ",sobrenome,"\n")
    		escreva("Você terá: ",idadeFim, " anos ao final do investimento\n")
    		escreva("Você investirá: R$ ",capital,"\n")
    		escreva("Seu patrimônio será de: R$ ",montante,"\n")
    	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 1265; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */