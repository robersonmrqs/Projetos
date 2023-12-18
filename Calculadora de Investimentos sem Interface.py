# Este código cria uma calculadora de investimentos sem interface gráfica
# Criado por Roberson Marques
# Data: 10/12/23

# Entrada de dados

nome = input("Digite o seu nome: ")
sobrenome = input("Digite seu sobrenome: ")
idade = input("Digite a sua idade: ")
valor_inicial = input("Digite o valor inicial: R$ ")
valor_posterior = input("Digite o valor dos investimentos posteriores: R$ ")
periodo = input("O investimento será em (m)eses ou (a)nos?: ")
tempo = input("Digite a quantidade de meses ou anos: ")
juros = input("Digite o valor da taxa de juros (%): ")

# Cálculo

juros = float(juros) / 100
if periodo == "a":
    tempo = int(tempo) * 12
capital = (int(valor_inicial) + (int(valor_posterior)) * int(tempo))
contador = 0
calculo_exp = 0
calculo_exp1 = 0
while contador < int(tempo):
    if calculo_exp == 0:
        calculo_exp = 1 + juros
    else:
        calculo_exp = calculo_exp * (1 + juros)
    contador = contador + 1
calculo_exp1 = calculo_exp - 1
if valor_inicial == 0:
    valor_inicial = 1.0
montante = float(valor_inicial) * float(calculo_exp) + float(valor_posterior) * float(calculo_exp1) / juros
idade_final = int(idade) + (int(tempo) / 12)

# Saída de dados

print(f"Seu nome é: {nome} {sobrenome}")
print(f"Você terá: {idade_final} anos ao final do investimento")
print(f"V0cê investirá: R$ {capital:,.2f}")
print(f"Seu patrimònio será de: R$ {montante:,.2f}")
 
