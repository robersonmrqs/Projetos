# Este código cria uma calculadora de investimentos sem interface gráfica
# Criado por Roberson Marques
# Data: 10/12/23

# Importação de bibliotecas

import tkinter as tk
from tkinter import ttk

lista_periodo = ["meses", "anos"]

# Função para cálculo

def calcular():

    # Entrada de dados

    juros = entry_taxa.get()
    periodo = combobox_periodo.get()
    tempo = entry_periodo.get()
    valor_inicial = entry_valor_inicial.get()
    valor_posterior = entry_valor_posterior.get()
    idade = entry_idade.get()

    # Cálculo

    juros = float(juros) / 100
    if periodo == "anos":
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

    texto = f"Você terá: {idade_final} anos ao final do investimento\n Você investirá: R$ {capital:,.2f}\n Seu patrimònio será de: R$ {montante:,.2f}"
    texto_calculo["text"] = texto
# Montagem da interface

janela = tk.Tk()
janela.title("Calculadora de Investimentos")
label_valor_inicial = tk.Label(janela, text = "Valor inicial R$", relief = "flat", bg = "lightblue")
label_valor_inicial.grid(row = 1, column = 0, padx = 10, pady = 10)
entry_valor_inicial = tk.Entry()
entry_valor_inicial.grid(row = 1, column = 1, padx = 10, pady = 10)
label_valor_posterior = tk.Label(janela, text = "Valor posterior R$", relief = "flat", bg = "lightblue")
label_valor_posterior.grid(row = 1, column = 2, padx = 10, pady = 10)
entry_valor_posterior = tk.Entry()
entry_valor_posterior.grid(row = 1, column = 3, padx = 10, pady = 10)
label_periodo = tk.Label(janela, text = "Período", relief = "flat", bg = "lightblue")
label_periodo.grid(row = 2, column = 0, padx = 10, pady = 10)
entry_periodo = tk.Entry()
entry_periodo.grid(row = 2, column = 1, padx = 10, pady = 10)
combobox_periodo = ttk.Combobox(janela, values = lista_periodo)
combobox_periodo.grid(row = 2, column = 2, padx = 10, pady = 10)
label_taxa = tk.Label(janela, text = "Taxa %", relief = "flat", bg = "lightblue")
label_taxa.grid(row = 3, column = 0, padx = 10, pady = 10)
entry_taxa = tk.Entry()
entry_taxa.grid(row = 3, column = 1, padx = 10, pady = 10)
label_idade = tk.Label(janela, text = "Idade atual", relief = "flat", bg = "lightblue")
label_idade.grid(row = 3, column = 2, padx = 10, pady = 10)
entry_idade = tk.Entry()
entry_idade.grid(row = 3, column = 3, padx = 10, pady = 10)
botao_calcular = tk.Button(janela, text = "Calcular", activebackground = "lightgreen", command = calcular)
botao_calcular.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 4)
texto_calculo = tk.Label(janela, text = "")
texto_calculo.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 4)

janela.mainloop()