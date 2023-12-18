programa
{

	// Programa para cadastrar e excluir alunos e suas notas e gerar relatório contendo média e aprovação
	// Criado por Roberson Marques, Bianca Rodrigues e Denilson Cosme(Batman)
	// Data: 05\12\2023
	
	inclua biblioteca Arquivos --> arq
	inclua biblioteca Texto --> tx
	inclua biblioteca Tipos -->tp
	
	// Declaração de variáveis e constantes globais
	
	const cadeia caminhoNomes = "cadastroNomes.txt", caminhoNotas = "cadastroNotas.txt"
	real notas[10][4]
	inteiro tamanhoVetor = 0
	cadeia nomes[10]
	
	funcao abrir()
	{
		
		// Função para abrir arquivos
		
		// Declaração de variáveis locais
		
		inteiro i, j, arquivoNomes, arquivoNotas
		cadeia linhaNomes, linhaNotas
		
		se(arq.arquivo_existe(caminhoNomes) e arq.arquivo_existe(caminhoNotas))
		{
			arquivoNomes = arq.abrir_arquivo(caminhoNomes, arq.MODO_LEITURA)
			arquivoNotas = arq.abrir_arquivo(caminhoNotas, arq.MODO_LEITURA)
			para(i = 0; i < 10; i++)
			{
				linhaNomes = arq.ler_linha(arquivoNomes)
				se(linhaNomes == "")
				{
					pare
				}
				senao
				{
					tamanhoVetor++
					nomes[i] = linhaNomes
				}
				para(j = 0; j < 4; j++)
				{
					linhaNotas = arq.ler_linha(arquivoNotas)
					notas[i][j] = tp.cadeia_para_real(linhaNotas)
				}
			}	
			arq.fechar_arquivo(arquivoNotas)
			arq.fechar_arquivo(arquivoNomes)
		}
	}
	
	funcao salvar()
	{
		
		// Função para salvar arquivos
		
		// Declaração de variáveis locais
		
		inteiro i, j, arquivoNomes, arquivoNotas
		cadeia linhaNomes, linhaNotas
		
		arquivoNomes = arq.abrir_arquivo(caminhoNomes, arq.MODO_ESCRITA)
		arquivoNotas = arq.abrir_arquivo(caminhoNotas, arq.MODO_ESCRITA)
		para(i = 0; i < tamanhoVetor; i++)
		{
			linhaNomes = nomes[i]
			arq.escrever_linha(linhaNomes, arquivoNomes)
			para(j = 0; j < 4; j++)
			{
				linhaNotas = tp.real_para_cadeia(notas[i][j])
				arq.escrever_linha(linhaNotas, arquivoNotas)
			}
		}
		arq.fechar_arquivo(arquivoNomes)
		arq.fechar_arquivo(arquivoNotas)
	}
	
	funcao inicio()
	{

		// Esta função contem o menu de opções
		
		// Declaração de variáveis locais
		
		inteiro opcao, i
		logico continuar = verdadeiro

		abrir()
		enquanto(continuar)
		{
			inteiro posicaoAluno = 0
			escreva("	GERENCIAMENTO DE ALUNOS\n\n")
			escreva(" Escolha uma opção:\n\n")
			escreva("1. Cadastrar Aluno\t2. Cadastrar Notas\t3. Gerar Relatório\n\n4. Excluir Aluno\t0. Fechar\n\n")
			leia(opcao)
			limpa()
			se(opcao > 4)
			{
				escreva("Opção Inválida\n")
				espere()
			}
			senao
			{
				escolha(opcao)
				{
					caso 1:
					cadastrarAluno()
					espere()
					pare
					caso 2:
					posicaoAluno = verificarAluno()
					se(posicaoAluno != -1)
					{
						cadastrarNotas(posicaoAluno)	
					}
					espere()
					pare
					caso 3:
					posicaoAluno = verificarAluno()
					se(posicaoAluno != -1)
					{
						gerarRelatorio(posicaoAluno)
					}
					espere()
					pare
					caso 4:
					posicaoAluno = verificarAluno()
					se(posicaoAluno != -1)
					{
						excluirAluno(posicaoAluno)
					}
					espere()
					pare
					caso contrario:
					continuar = falso
					salvar()
				}
			}
			limpa()
		}
	}
	
	funcao cadastrarAluno()
	{

		// Função para cadastrar alunos
		
		// Declaração de variáveis locais
		
		inteiro i
		cadeia nome
		caracter opcao
		
		faca
		{
			escreva("\nDigite o nome do aluno: ")
			leia(nome)
			nome = tx.caixa_baixa(nome)
			nomes[tamanhoVetor] = nome
			tamanhoVetor++
			escreva("\nAluno adicionado com sucesso \n\n")
			escreva("Deseja cadastrar mais alunos? (s)im ou (n)ao: ")
			leia(opcao)
			limpa()
		}
		enquanto(opcao != 'n')
	}
	
	funcao espere()
	{
		
		// Esta função faz o programa esperar a ação do usuário
		
		// Declaração de variável local
		
		cadeia _
		
		escreva("\nPressione enter para continuar...")
		leia(_)
	}

	funcao inteiro verificarAluno()
	{
		
		// Função para pesquisar o vetor Nomes
		
		// Declaração de variáveis locais

		inteiro i
		cadeia nome
		
		escreva("Digite o nome do Aluno: ")
		leia(nome)
		limpa()
		para(i = 0; i < tamanhoVetor; i++)
		{
			se(nomes[i] == nome)
			{
				retorne i
			}
		}
		escreva("Aluno não encontrado \n")
		retorne -1
	}

	funcao cadastrarNotas(inteiro posicaoNome)
	{
		// Função para cadastrar notas
		
		// Declaração de váriaveis locais

		inteiro i
		cadeia restoNome = tx.extrair_subtexto(nomes[posicaoNome], 1, tx.numero_caracteres(nomes[posicaoNome])), primeiraLetra = tx.caixa_alta(tp.caracter_para_cadeia(tx.obter_caracter(nomes[posicaoNome], 0)))
		
		para(i = 0; i < 4; i++)
		{
			escreva("Digite a nota do ", i + 1,"º bimestre para ", primeiraLetra + restoNome,": ")
			leia(notas[posicaoNome][i])
		}
		escreva("\nNotas cadastradas com sucesso \n")	
	}
	
	funcao gerarRelatorio(inteiro posicaoNome)
	{

		// Função para Gerar o relatório de notas contendo média e aprovação
		
		// Declaração de variáveis locais
		
		real medias, sum = 0.0
		inteiro c
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

	funcao excluirAluno(inteiro posicaoIndice)
	{

		// Função para excluir alunos
		
		// Declaração de variáveis locais

		inteiro i, j
		cadeia nome

		para(i = posicaoIndice; i < tamanhoVetor-1; i++)
		{
			nomes[i] = nomes[i+1]
			para(j = 0; j < 4; j++)
			{
				notas[i][j] = notas[i+1][j]
			}
		}
		tamanhoVetor--
		escreva("\nAluno removido com sucesso!\n")
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 5908; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = {notas, 15, 6, 5}-{nomes, 17, 8, 5};
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */