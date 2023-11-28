programa
{
	inclua biblioteca Arquivos

	// Programa para cadastrar alunos, notas e gerar relatório contendo média e aprovação
	// Criado por Roberson Marques
	// Data: 27/11/2023
	
	// Declaração de variáveis globais
	
	cadeia nomes[10]
	real notas[10][4]
	
	funcao inicio()
	{

		// Esta função contem o meu de opções
		// Declaração de variáveis locais
		
		inteiro opcao
		logico continuar = verdadeiro
		
		enquanto(continuar)
		{
			escreva("	GERENCIAMENTO DE ALUNOS\n\n")
			escreva(" Escolha uma opção:\n\n")
			escreva("1. Cadastrar Aluno\t3. Gerar relatório\n\n2. Cadastrar Notas\t4. Fechar\n\n")
			leia(opcao)
			limpa()
			escolha(opcao)
			{
				caso 1:
				cadastrarAluno()
				espere()
				pare
				caso 2:
				verificarAluno()
				espere()
				pare
				caso 3:
				verificarAlunoRelatorio()
				espere()
				pare
				caso contrario:
				continuar = falso
			}
			limpa()
		}
	}
	
	funcao cadastrarAluno()
	{

		// Função para cadastrar alunos
		// Declaração de variáveis locais
		
		cadeia nome
		inteiro i
		
		escreva("\nDigite o nome do aluno: ")
		leia(nome)
		para(i = 0; i < 10; i++)
		{
			se(nomes[i] == "")
			{
				nomes[i] = nome
				pare
			}
		}
		escreva("\nAluno adicionado com sucesso \n")
	}
	
	funcao espere()
	{
		
		// Esta função cria faz o programa esperar a ação do usuário
		// Declaração de variável local
		
		cadeia _
		
		escreva("\nPressione enter para continuar...")
		leia(_)
	}

	funcao verificarAluno()
	{
		
		// Função para pesquisar o vetor
		// Declaração de variáveis locais
		
		cadeia nome
		logico encontrado = falso
		inteiro i
		
		escreva("Digite o nome do Aluno: ")
		leia(nome)
		limpa()
		para(i = 0; i < 10; i++)
		{
			se(nomes[i] == nome)
			{
				encontrado = verdadeiro
				cadastrarNotas(i)
				pare
			}
		}

		se (encontrado == falso){
			escreva("Aluno não encontrado \n")
		}
	}

	funcao verificarAlunoRelatorio()
	{
		
		// Função para pesquisar o vetor
		// Declaração de variáveis locais
		
		cadeia nome
		logico encontrado = falso
		inteiro i
		
		escreva("Digite o nome do Aluno: ")
		leia(nome)
		limpa()
		para(i = 0; i < 10; i++)
		{
			se(nomes[i] == nome)
			{
				encontrado = verdadeiro
				geraRelatorio(i)
				pare
			}
		}

		se (encontrado == falso){
			escreva("Aluno não encontrado \n")
		}
	}

	funcao cadastrarNotas(inteiro posicaoNome)
	{
		// Função para cadastrar notas
		// Declaração de váriaveis locais
		escreva("Digite a note do 1º bimestre para ", nomes[posicaoNome],": ")
		leia(notas[posicaoNome][0])
		limpa()
		
		escreva("Digite a note do 2º bimestre para ", nomes[posicaoNome],": ")
		leia(notas[posicaoNome][1])
		limpa()
		
		escreva("Digite a note do 3º bimestre para ", nomes[posicaoNome],": ")
		leia(notas[posicaoNome][2])
		limpa()
		
		escreva("Digite a note do 4º bimestre para ", nomes[posicaoNome],": ")
		leia(notas[posicaoNome][3])
		limpa()
		
		escreva("Notas cadastradas com sucesso \n")
	}
	
	funcao geraRelatorio(inteiro posicaoNome)
	{

		// Função para Gerar o relatório de notas contendo média e aprovação
		// Declaração de variáveis locais
		
		real medias, sum = 0.0
		inteiro c, aluno
		cadeia apr
		
		para(c = 0; c < 4; c++)
		{
			sum += notas[posicaoNome][c]
		}
		medias = sum / 4
		
		limpa()
		
		se(medias >= 6)
		{
			apr = "APROVADO"
		}
		senao
		{
			apr = "REPROVADO"
		}
	
		escreva("=========================","\n")
		escreva("	Aluno: "+ nomes[posicaoNome],"\n")
		escreva("-------------------------","\n")
		escreva("	1B : "+notas[posicaoNome][0],"\n")
		escreva("	2B : "+notas[posicaoNome][1],"\n")
		escreva("	3B : "+notas[posicaoNome][2],"\n")
		escreva("	4B : "+notas[posicaoNome][3],"\n")
		escreva("-------------------------","\n")
		escreva("	Média : "+medias,"\n")
		escreva("	"+apr,"\n")
		escreva("=========================\n")
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 2321; 
 * @DOBRAMENTO-CODIGO = [13, 50, 72, 84, 112, 140];
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = {nomes, 11, 8, 5}-{notas, 12, 6, 5};
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */
