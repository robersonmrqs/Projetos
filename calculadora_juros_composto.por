programa
{

	// Programa para calcular juros composto
	// Criado por Roberson Marques
	// Data: 24/09/2023
	
	funcao inicio()
	{
	
	// Declaração de variáveis
	
	inteiro tempo, i
	real capital, juros, montante
	
	escreva("Digite o capital: ")
	leia(capital)
	escreva("Digite o valor da taxa (%): ")
	leia(juros)
	escreva("Digite a quantidade de meses: ")
	leia(tempo)
	limpa()

	juros = juros / 100
	montante = capital * (1 + juros)
	para(i = 1; i <= tempo; i++)
		{
		escreva("Seu montante será: ",montante,"\n")
		montante = montante + (montante * juros)
		}
	
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 106; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */