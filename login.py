import tkinter as tk
import customtkinter as ctk
import mysql.connector as mc
import re
import requests
import pandas as pd
import json
from CTkToolTip import *
from tkinter import messagebox, Toplevel, Scrollbar, Text, VERTICAL, Y
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def validacao_cpf(cpf):
    cpf = re.sub('[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    total = 0
    
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    total = 0
    
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    return int(cpf[9]) == digit1 and int(cpf[10]) == digit2

def validar_email(email):
    return "@" in email

class TelaLogin():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Login de Usuário")
        self.janela.geometry("400x350")
        self.janela.resizable(False, False)
        self.janela.bind('<Return>', lambda event = None: self.login())

        self.frame_login = ctk.CTkFrame(janela)

        self.cabecalho= ctk.CTkLabel(self.janela, text = "FAÇA SEU LOGIN", font = ("verdana", 20), text_color = "blue")
        self.cabecalho.place(x = 110, y = 10)
        self.usuario = ctk.CTkEntry(self.janela, placeholder_text = "Digite seu username", font = ("verdana", 14), justify = "center", width = 300)
        self.usuario.place(x = 50, y = 70)
        self.texto1 = ctk.CTkLabel(self.janela, text = "*campo obrigatório", font = ("verdana", 10), text_color = "green")
        self.texto1.place(x = 50, y = 100)
        self.senha = ctk.CTkEntry(self.janela, placeholder_text = "Digite sua senha", font = ("verdana", 14), justify = "center", width = 300, show = "*")
        self.senha.place(x = 50, y = 130)
        self.texto2 = ctk.CTkLabel(self.janela, text = "*campo obrigatório", font = ("verdana", 10), text_color = "green")
        self.texto2.place(x = 50, y = 160)
        self.check_box = ctk.IntVar()
        self.checkbox = ctk.CTkCheckBox(self.janela, text = "Lembrar", font = ("verdana", 14), variable = self.check_box)
        self.checkbox.place(x = 50, y = 200)
        self.botao_login = ctk.CTkButton(self.janela, text = "Login", font = ("verdana", 16), width = 200, command = self.login)
        self.botao_login.place(x = 100, y = 250)
        self.texto3 = ctk.CTkLabel(self.janela, text = "Não tem cadastro?", font = ("verdana", 14))
        self.texto3.place(x = 80, y = 310)
        self.botao_cadastro = ctk.CTkButton(self.janela, text = "Clique aqui", font = ("verdana", 14), fg_color = "transparent", hover_color = "green", width = 30, command = self.cad_usuario)
        self.botao_cadastro.place(x = 220, y = 310)
        self.load_saved_user()

    def load_saved_user(self):
        try:
            with open("saved_user.json", "r") as file:
                saved_user_data = json.load(file)
                self.usuario.insert(0, saved_user_data.get("username", ""))
                self.senha.insert(0, saved_user_data.get("password", ""))
                self.check_box.set(saved_user_data.get("remember", 0))
        except FileNotFoundError:
            pass

    def save_user_data(self):
        user_data = {"username": self.usuario.get(), "password": self.senha.get(), "remember": self.check_box.get()}
        with open("saved_user.json", "w") as file:
            json.dump(user_data, file)

    def login(self):
        usuario = self.usuario.get()
        senha = self.senha.get()
    
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_usuarios")
        cursor = conexao.cursor()
        comando = f"SELECT * FROM usuario WHERE usuario = '{usuario}' AND senha = '{senha}'"
        cursor.execute(comando)
        bd = cursor.fetchone()
        cursor.close()
        conexao.close()
        
        if bd:
            messagebox.showinfo(title = "Login de usuário", message = "Login efetuado com sucesso!")
            if self.check_box.get():
                self.save_user_data()
            self.tela_opcao()
        else:
            messagebox.showerror(title = "Login de usuário", message = "Usuário e ou senha não encontrados!")
            self.usuario.delete(0, 'end')
            self.senha.delete(0, 'end')

    def tela_opcao(self):
        TelaOpcao(self.janela)

    def cad_usuario(self):
        TelaCadastrarUsuario(self.janela)

class TelaOpcao():
    def __init__(self, janela):
        self.janela_principal = janela
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Tela de Opções")
        self.janela.geometry("350x330")
        self.janela.resizable(False, False)
        self.janela.transient(janela)

        self.frame_opcao = ctk.CTkFrame(self.janela)

        self.cabecalho = ctk.CTkLabel(self.janela, text = "ESCOLHA UMA OPÇÃO", font = ("verdana", 20), text_color = "blue")
        self.cabecalho.place(x = 60, y = 10)
        self.botao_cadastro = ctk.CTkButton(self.janela, text = "Cadastrar Aluno", font = ("verdana", 16), fg_color = "green", width = 200, command = self.cad_aluno)
        self.botao_cadastro.place(x = 75, y = 70)
        self.botao_cad_notas = ctk.CTkButton(self.janela, text = "Cadastrar Notas", font = ("verdana", 16), fg_color = "green", width = 200, command = self.cad_notas)
        self.botao_cad_notas.place(x = 75, y = 120)
        self.botao_gera_relat = ctk.CTkButton(self.janela, text = "Gerar Relatório", font = ('verdana', 16), fg_color = "green", width = 200, command = self.gera_rel)
        self.botao_gera_relat.place(x = 75, y = 170)
        self.botao_excluir = ctk.CTkButton(self.janela, text = "Excluir Aluno", font = ('verdana', 16), fg_color = "green", width = 200, command = self.exc_aluno)
        self.botao_excluir.place(x = 75, y = 220)
        self.botao_encerrar = ctk.CTkButton(self.janela, text = "Encerrar Sistema", font = ("verdana", 14), width = 150, command = self.encerrar_sistema)
        self.botao_encerrar.place(x = 100, y = 280)

    def encerrar_sistema(self):
        self.janela_principal.destroy()

    def cad_aluno(self):
        TelaCadastrarAluno(self.janela)

    def cad_notas(self):
        TelaCadastrarNotas(self.janela)

    def gera_rel(self):
        TelaGerarRelatorio(self.janela)

    def exc_aluno(self):
        TelaExcluirAluno(self.janela)

class TelaCadastrarUsuario():
    def __init__(self, janela):
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Cadastro de Usuário")
        self.janela.geometry("400x420")
        self.janela.resizable(False, False)
        self.janela.transient(janela)

        self.frame_cadastrar_usuario = ctk.CTkFrame(self.janela)

        self.cabecalho = ctk.CTkLabel(self.janela, text = "FAÇA SEU CADASTRO", font = ("verdana", 20), text_color = "blue")
        self.cabecalho.place(x = 90, y = 10)
        self.texto1 = ctk.CTkLabel(self.janela, text = "*Todos os campos são obrigatórios", font = ("verdana", 10),text_color = "green")
        self.texto1.place(x = 50, y = 50)
        self.nome = ctk.CTkEntry(self.janela, placeholder_text = "Digite seu nome completo", font = ("verdana", 14), justify = "center", width = 300)
        self.nome.place(x = 50, y = 90)
        self.email = ctk.CTkEntry(self.janela, placeholder_text = "Digite seu email", font = ("verdana", 14), justify = "center", width = 300)
        self.email.place(x = 50, y = 130)
        self.usuario = ctk.CTkEntry(self.janela, placeholder_text = "Digite seu username", font = ("verdana", 14), justify = "center", width = 300)
        self.usuario.place(x = 50, y = 190)
        self.senha = ctk.CTkEntry(self.janela, placeholder_text = "Digite sua senha", font = ("verdana", 14), justify = "center", width = 300, show = "*")
        self.senha.place(x = 50, y =230)
        self.texto_tooltip = "Máximo 10 caracteres, ao menos uma letra maiúscula e um número"
        self.tooltip = CTkToolTip(self.senha, message = self.texto_tooltip)
        self.confirma = ctk.CTkEntry(self.janela, placeholder_text = "Confirme sua senha", font = ("verdana", 14), justify = "center", width = 300, show = "*")
        self.confirma.place(x = 50, y =270)
        self.checkbox = ctk.CTkCheckBox(self.janela, text = "Aceito os termos e políticas", font = ("verdana", 14))
        self.checkbox.place(x = 50, y = 320)
        self.botao_cadastrar = ctk.CTkButton(self.janela, text = "Cadastrar", font = ("verdana", 16), width = 140, command = self.cadastro)
        self.botao_cadastrar.place(x = 210, y = 370)
        self.botao_voltar = ctk.CTkButton(self.janela, text = "Voltar", font = ("verdana", 16), fg_color = "green", width = 140, command = self.janela.destroy)
        self.botao_voltar.place(x = 50, y = 370)
        self.senha.bind("<FocusIn>", self.mostrar_tooltip)
        self.senha.bind("<FocusOut>", self.ocultar_tooltip)
        self.checkbox.bind("<Button-1>", self.checkbox_changed)

    def checkbox_changed(self, event):
        if self.checkbox.get() == 1:
            self.mostrar_acordos()

    def mostrar_acordos(self):
        self.janela = ctk.CTkToplevel(self.janela)
        self.janela.title("Termos e Políticas")
        self.janela.geometry("350x350")
        self.janela.resizable(False, False)
        self.janela.grab_set()

        try:
            with open('termos_e_politicas.txt', 'r', encoding = 'utf-8') as file:
                texto_acordos = file.read()
        except FileNotFoundError:
            texto_acordos = "Erro ao carregar os termos e políticas."

        self.scrollbar = Scrollbar(self.janela, orient = VERTICAL)
        self.scrollbar.pack(side = "right", fill = Y)
        self.texto = Text(self.janela, wrap = "word", yscrollcommand = self.scrollbar.set, width = 50, height = 20)
        self.texto.insert("1.0", texto_acordos)
        self.texto.pack(padx = 10, pady = 10)
        self.scrollbar.config(command = self.texto.yview)
        self.aceitar = ctk.CTkButton(self.janela, text = "Aceitar", command = self.janela.destroy)
        self.aceitar.pack(side = "left", padx = 10)
        self.negar = ctk.CTkButton(self.janela, text = "Negar", command = self.fechar_acordos)
        self.negar.pack(side = "right", padx = 10)

    def fechar_acordos(self):
        self.checkbox.deselect()
        self.janela.destroy()
        self.janela.grab_release()

    def checar_senha(self, password):
        if len(password) > 10:
            return False
        elif not any(char.isupper() for char in password):
            return False
        elif not any(char.isdigit() for char in password):
            return False
        else:
            return True

    def cadastro(self):
        nome = self.nome.get()
        email = self.email.get()
        usuario = self.usuario.get()
        senha = self.senha.get()
        confirma_senha = self.confirma.get()
        
        if not self.checar_senha(senha):
            messagebox.showerror(title = "Cadastro de usuário", message = "A senha não atende aos requisitos.")
            return
        if not nome or not email or not usuario or not senha or not confirma_senha:
            messagebox.showerror(title = "Cadastro de usuário", message = "Por favor, preencha todos os campos.")
        elif senha != confirma_senha:
            messagebox.showerror(title = "Cadastro de usuário", message = "Senhas não conferem!")
        elif not validar_email(email):
            messagebox.showerror(title = "Cadastro de usuário", message = "Email inválido!")
        else:
            conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_usuarios")
            cursor = conexao.cursor()
            comando = f"INSERT INTO usuario (nome, email, usuario, senha) VALUES ('{nome}', '{email}', '{usuario}', '{senha}')"
            cursor.execute(comando)
            conexao.commit()
            messagebox.showinfo(title = "Cadastro de usuário", message = "Usuário cadastrado com sucesso!")
            self.nome.delete(0, 'end')
            self.email.delete(0, 'end')
            self.usuario.delete(0, 'end')
            self.senha.delete(0, 'end')
            self.confirma.delete(0, 'end')
            cursor.close()
            conexao.close()

    def mostrar_tooltip(self, event):
        self.tooltip.show()

    def ocultar_tooltip(self, event):
        self.tooltip.hide()

class CTkToolTip:
    def __init__(self, widget, message):
        self.widget = widget
        self.message = message
        self.tooltip = None

    def show(self):
        if self.tooltip is not None:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 30
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text = self.message, background = "#ffffe0", justify = tk.LEFT, relief = tk.SOLID,
                         borderwidth = 1, font = ("Verdana", 14))
        label.pack(ipadx=1)

    def hide(self):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

class TelaCadastrarAluno():
    def __init__(self, janela):
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Cadastro de Aluno")
        self.janela.geometry("700x700")
        self.janela.resizable(False, False)
        self.janela.transient(janela)

        self.frame_cadastrar_aluno = ctk.CTkFrame(self.janela)

        self.cabecalho = ctk.CTkLabel(self.janela, text = "CADASTRO DE ALUNOS", font = ("verdana", 28), text_color = "blue")
        self.cabecalho.place(x = 200, y = 10)
        self.texto1 = ctk.CTkLabel(self.janela, text = "*Todos os campos são obrigatórios", font = ("verdana", 12), text_color = "green")
        self.texto1.place(x = 50, y = 60)
        self.texto2 = ctk.CTkLabel(self.janela, text = "Informações do Aluno", font = ("verdana", 14), text_color = "blue")
        self.texto2.place(x = 50, y = 100)
        self.nome = ctk.CTkEntry(self.janela, placeholder_text = "Nome completo", font = ("verdana", 16), justify = "center", width = 600)
        self.nome.place(x = 50, y = 140)
        self.cep = ctk.CTkEntry(self.janela, placeholder_text = "CEP", font = ("verdana", 16), justify = "center", width = 120)
        self.cep.place(x=50, y=190)
        self.botao_buscar_cep = ctk.CTkButton(self.janela, text = "Buscar CEP", font = ("verdana", 16), width = 100, command = self.buscar_cep)
        self.botao_buscar_cep.place(x=190, y=190)
        self.endereco = ctk.CTkEntry(self.janela, placeholder_text = "Endereço", font = ("verdana", 16), justify = "center", width = 335)
        self.endereco.place(x = 315, y = 190)
        self.numero_endereco = ctk.CTkEntry(self.janela, placeholder_text = "Número", font = ("verdana", 16), justify = "center", width = 90)
        self.numero_endereco.place(x = 50, y = 240)
        self.bairro = ctk.CTkEntry(self.janela, placeholder_text = "Bairro", font = ("verdana", 16), justify = "center", width = 240)
        self.bairro.place(x = 155, y = 240)
        self.localidade = ctk.CTkEntry(self.janela, placeholder_text = "Cidade", font = ("verdana", 16), justify = "center", width = 240)
        self.localidade.place(x = 408, y = 240)
        self.email = ctk.CTkEntry(self.janela, placeholder_text = "Email", font = ("verdana", 16), justify = "center", width = 600)
        self.email.place(x = 50, y = 290)
        self.idade = ctk.CTkEntry(self.janela, placeholder_text = "Idade", font = ("verdana", 16), justify = "center", width = 80)
        self.idade.place(x = 50, y = 340)
        self.tipo_doc = ctk.CTkLabel(self.janela, text = "Tipo documento:", font = ("verdana", 16), justify = "center", width = 160, text_color = "blue")
        self.tipo_doc.place(x = 135, y = 340)
        self.comb_doc = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", width = 80, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["RG", "CPF"])
        self.comb_doc.place(x = 300, y = 340)
        self.num_doc = ctk.CTkLabel(self.janela, text = "Numº:", font = ("verdana", 16), justify = "center", width = 50, text_color = "blue")
        self.num_doc.place(x = 395, y = 340)
        self.numero_doc = ctk.CTkEntry(self.janela, placeholder_text = "Somente números", font = ("verdana", 16), justify = "center", width = 190)
        self.numero_doc.place(x = 460, y = 340)
        self.telefone = ctk.CTkEntry(self.janela, placeholder_text = "Telefone", font = ("verdana", 16), justify = "center", width = 200)
        self.telefone.place(x = 50, y = 390)
        self.genero = ctk.CTkLabel(self.janela, text = "Genero:", font = ("verdana", 16), justify = "center", width = 110, text_color = "blue")
        self.genero.place(x = 250, y = 390)
        self.comb_gen = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["Masculino", "Feminino", "Sem gênero"])
        self.comb_gen.place(x = 350, y = 390)
        self.pcd = ctk.CTkLabel(self.janela, text = "PCD:", font = ("verdana", 16), justify = "center", width = 50, text_color = "blue")
        self.pcd.place(x = 502, y = 390)
        self.comb_pcd = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", width = 90, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["Sim", "Não"])
        self.comb_pcd.place(x = 560, y = 390)
        self.texto3 = ctk.CTkLabel(self.janela, text = "Informações do Curso", font = ("verdana", 14), text_color = "blue")
        self.texto3.place(x = 50, y = 440)
        self.curso = ctk.CTkEntry(self.janela, placeholder_text = "Nome do curso", font = ("verdana", 16), justify = "center", width = 600)
        self.curso.place(x = 50, y = 480)
        self.turma = ctk.CTkLabel(self.janela, text = "Turma:", font = ("verdana", 16), justify = "left", text_color = "blue")
        self.turma.place(x = 50, y = 530)
        self.comb_turma = ctk.CTkComboBox(self.janela, font = ("verdana", 16), width = 150, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["1º Semestre", "2º Semestre"])
        self.comb_turma.place(x = 120, y = 530)
        self.turno = ctk.CTkLabel(self.janela, text = "Turno:", font = ("verdana", 16), justify = "center", text_color = "blue")
        self.turno.place(x = 280, y = 530)
        self.comb_turno = ctk.CTkComboBox(self.janela, font = ("verdana", 16), width = 100, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["Manhã", "Tarde", "Noite"])
        self.comb_turno.place(x = 345, y = 530)
        self.transferido = ctk.CTkLabel(self.janela, text = "Transferido:", font = ("verdana", 16), justify = "center", text_color = "blue")
        self.transferido.place(x = 455, y = 530)
        self.comb_transf = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", width = 90, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["Sim", "Não"])
        self.comb_transf.place(x = 560, y = 530)
        self.botao_cad_aluno = ctk.CTkButton(self.janela, text = "Cadastrar Aluno", font = ("verdana", 24), height = 50, width = 400, command = self.cadastro)
        self.botao_cad_aluno.place(x = 150, y = 580)
        self.botao_voltar = ctk.CTkButton(self.janela, text = "Voltar", font = ("verdana", 16), fg_color = "green", width = 140, command = self.janela.destroy)
        self.botao_voltar.place(x = 280, y = 650)

    def cadastro(self):
        nome = self.nome.get()
        endereco = f"{self.endereco.get()} {self.numero_endereco.get()} {self.bairro.get()} {self.localidade.get()} {self.cep.get()}"
        email = self.email.get()
        telefone = self.telefone.get()
        genero = self.comb_gen.get()
        pcd = self.comb_pcd.get()
        curso = self.curso.get()
        turma = self.comb_turma.get()
        turno = self.comb_turno.get()
        idade = self.idade.get()
        tipodoc = self.comb_doc.get()
        numerodoc = self.numero_doc.get()
        transf = self.comb_transf.get()

        if not nome or not endereco or not email or not telefone or not genero or not pcd or not curso or not turma or not turno or not idade or not tipodoc or not numerodoc or not transf:
            messagebox.showerror(title  =   "Cadastro de aluno", message = "Por favor, preencha todos os campos.")        
        elif self.comb_doc.get() == "CPF" and not validacao_cpf(numerodoc):
            messagebox.showerror(title = "Cadastro de aluno", message = "CPF inválido. Por favor, insira um CPF válido.")
            return
        elif not validar_email(email):
            messagebox.showerror(title = "Cadastro de aluno", message = "Email inválido!")
        else:
            conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_alunos")
            cursor = conexao.cursor()
            consulta_aluno = f"SELECT * FROM aluno WHERE numerodoc = '{numerodoc}'"
            cursor.execute(consulta_aluno)
            aluno_existente = cursor.fetchone()

        if aluno_existente:
            messagebox.showerror(title = "Cadastro de aluno", message = "Aluno já cadastrado com este número de documento.")
        else:
            comando = f"INSERT INTO aluno (nome, endereco, email, telefone, genero, pcd, curso, turma, turno, idade, tipodoc, numerodoc, transf) VALUES ('{nome}', '{endereco}', '{email}', '{telefone}', '{genero}', '{pcd}', '{curso}', '{turma}', '{turno}', '{idade}', '{tipodoc}', '{numerodoc}', '{transf}')"
            cursor.execute(comando)
            conexao.commit()
            messagebox.showinfo(title = "Cadastro de aluno", message = "Aluno cadastrado com sucesso!")
            self.nome.delete(0, 'end')
            self.cep.delete(0 , 'end')
            self.endereco.delete(0, 'end')
            self.numero_endereco.delete(0, 'end')
            self.bairro.delete(0, 'end')
            self.localidade.delete(0, 'end')
            self.email.delete(0, 'end')
            self.telefone.delete(0, 'end')
            self.curso.delete(0, 'end')
            self.idade.delete(0, 'end')
            self.numero_doc.delete(0, 'end')
            cursor.close()
            conexao.close()
    
    def buscar_cep(self):
        cep = self.cep.get()
        
        if not cep:
            messagebox.showwarning("Aviso", "Por favor, insira um CEP.")
            return

        try:
            resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            data = resposta.json()
            if "erro" not in data:
                # Preenche os campos de endereço com os dados obtidos
                self.endereco.delete(0, 'end')
                self.endereco.insert(0, data.get("logradouro", ""))
                self.bairro.delete(0, 'end')
                self.bairro.insert(0, data.get("bairro", ""))
                self.localidade.delete(0, 'end')
                self.localidade.insert(0, data.get("localidade", ""))
                messagebox.showinfo("Informação", "CEP encontrado com sucesso.")
            else:
                messagebox.showwarning(title = "Cadastro de aluno", message = "CEP não encontrado. Por favor, verifique o CEP e tente novamente.")

        except Exception as e:
            print(f"Erro ao buscar CEP: {e}")
            messagebox.showerror(title = "Cadastro de aluno", message = "Ocorreu um erro ao buscar o CEP. Tente novamente.")
            
class TelaCadastrarNotas():
    def __init__(self, janela):
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Cadastro de Notas")
        self.janela.geometry("700x740")
        self.janela.resizable(False, False)
        self.janela.transient(janela)
        self.janela.bind('<Return>', lambda event = None: self.pesquisar())

        self.frame_cadastrar_notas = ctk.CTkFrame(self.janela)
        
        self.cabecalho = ctk.CTkLabel(self.janela, text = "CADASTRO DE MATERIAS E NOTAS", font = ("verdana", 28), text_color = "blue")
        self.cabecalho.place(x = 100, y = 10)
        self.tipo_doc = ctk.CTkLabel(self.janela, text = "Tipo documento:", font = ("verdana", 16), justify = "center", width = 160, text_color = "blue")
        self.tipo_doc.place(x = 30, y = 60)
        self.comb_doc = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", width = 80, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["RG", "CPF"])
        self.comb_doc.place(x = 190, y = 60)
        self.num_cpf = ctk.CTkLabel(self.janela, text = "Núm:", font = ("verdana", 16), text_color = "blue")
        self.num_cpf.place(x = 285, y = 60)
        self.numero_doc = ctk.CTkEntry(self.janela, placeholder_text = "Somente números", font = ("verdana", 16), justify = "center", width = 190)
        self.numero_doc.place(x = 345, y = 60)
        self.botao_pesquisar = ctk.CTkButton(self.janela, text = "Pesquisar", font = ("verdana", 16), width = 100, fg_color = "green", command = self.pesquisar)
        self.botao_pesquisar.place(x = 550, y = 60)
        self.nome = ctk.CTkLabel(self.janela, text = "", font = ("verdana", 16), justify = "center", width = 600)
        self.nome.place(x = 50, y = 110)
        self.curso = ctk.CTkLabel(self.janela, text = "", font = ("verdana", 16), justify = "center", width = 600)
        self.curso.place(x = 50, y = 160)
        self.texto1 = ctk.CTkLabel(self.janela, text = "Cadastro de Materias", font = ("verdana", 16), text_color = "green")
        self.texto1.place(x = 120, y = 210)
        self.texto2 = ctk.CTkLabel(self.janela, text = "Cadastro de Notas", font = ("verdana", 16), text_color = "green")
        self.texto2.place(x = 490, y = 210)
        self.texto3 = ctk.CTkLabel(self.janela, text = "1º Bim 2º Bim 3º Bim 4º Bim", font = ("verdana", 16), text_color = "white")
        self.texto3.place(x = 440, y = 260)
        self.materia1 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 1", font = ("verdana", 16), justify = "center", width = 380)
        self.materia1.place(x = 20, y = 310)
        self.materia2 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 2", font = ("verdana", 16), justify = "center", width = 380)
        self.materia2.place(x = 20, y = 360)
        self.materia3 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 3", font = ("verdana", 16), justify = "center", width = 380)
        self.materia3.place(x = 20, y = 410)
        self.materia4 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 4", font = ("verdana", 16), justify = "center", width = 380)
        self.materia4.place(x = 20, y = 460)
        self.materia5 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 5", font = ("verdana", 16), justify = "center", width = 380)
        self.materia5.place(x = 20, y = 510)
        self.materia6 = ctk.CTkEntry(self.janela, placeholder_text = "Materia 6", font = ("verdana", 16), justify = "center", width = 380)
        self.materia6.place(x = 20, y = 560)
        self.m1n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m1n1.place(x = 445, y = 310)
        self.m1n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m1n2.place(x = 506, y = 310)
        self.m1n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m1n3.place(x = 567, y = 310)
        self.m1n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m1n4.place(x = 629, y = 310)
        self.m2n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m2n1.place(x = 445, y = 360)
        self.m2n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m2n2.place(x = 506, y = 360)
        self.m2n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m2n3.place(x = 567, y = 360)
        self.m2n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m2n4.place(x = 629, y = 360)
        self.m3n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m3n1.place(x = 445, y = 410)
        self.m3n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m3n2.place(x = 506, y = 410)
        self.m3n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m3n3.place(x = 567, y = 410)
        self.m3n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m3n4.place(x = 629, y = 410)
        self.m4n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m4n1.place(x = 445, y = 460)
        self.m4n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m4n2.place(x = 506, y = 460)
        self.m4n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m4n3.place(x = 567, y = 460)
        self.m4n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m4n4.place(x = 629, y = 460)
        self.m5n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m5n1.place(x = 445, y = 510)
        self.m5n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m5n2.place(x = 506, y = 510)
        self.m5n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m5n3.place(x = 567, y = 510)
        self.m5n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m5n4.place(x = 629, y = 510)
        self.m6n1 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m6n1.place(x = 445, y = 560)
        self.m6n2 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m6n2.place(x = 506, y = 560)
        self.m6n3 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m6n3.place(x = 567, y = 560)
        self.m6n4 = ctk.CTkEntry(self.janela, placeholder_text = "", font = ("verdana", 16), justify = "center", width = 50)
        self.m6n4.place(x = 629, y = 560)
        self.botao_cadastro = ctk.CTkButton(self.janela, text = "Cadastrar", font = ("verdana", 24), height = 50, width = 400, command = self.cadastro)
        self.botao_cadastro.place(x = 150, y = 615)
        self.botao_voltar = ctk.CTkButton(self.janela, text = "Voltar", font = ("verdana", 16), fg_color = "green", width = 140, command = self.janela.destroy)
        self.botao_voltar.place(x = 280, y = 690)
        self.nome_aluno = ""
        self.curso_aluno = ""

    def pesquisar(self):
        if self.comb_doc.get() == "CPF" and not validacao_cpf(self.numero_doc.get()):
            messagebox.showerror(title = "Cadastro de Notas", message = "CPF inválido. Por favor, insira um CPF válido.")
            return
        
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_alunos")
        cursor = conexao.cursor()
        consulta_aluno = f"SELECT nome, curso FROM aluno WHERE numerodoc = '{self.numero_doc.get()}'"
        cursor.execute(consulta_aluno)
        aluno_existente = cursor.fetchone()

        if not aluno_existente:
            messagebox.showerror(title = "Cadastro de notas", message = "Aluno não encontrado com este número de documento.")
        else:
            self.nome_aluno = aluno_existente[0]
            self.curso_aluno = aluno_existente[1]
            self.nome.configure(text = f"{self.nome_aluno}", justify = "center", width = 600)
            self.curso.configure(text = f"{self.curso_aluno}", justify = "center", width = 600)

    def cadastro(self):
        materia1 = self.materia1.get()
        materia2 = self.materia2.get()
        materia3 = self.materia3.get()
        materia4 = self.materia4.get()
        materia5 = self.materia5.get()
        materia6 = self.materia6.get()
        
        val_matriz = []

        for i in range(1, 7):
            val_linha = []
            for j in range(1, 5):
                valor = getattr(self, f"m{i}n{j}").get()
                val_linha.append(valor)
            val_matriz.append(val_linha)

        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_materias")
        cursor = conexao.cursor()
        nomes_materias = [self.materia1.get(), self.materia2.get(), self.materia3.get(), self.materia4.get(), self.materia5.get(), self.materia6.get()]
        comando_materias = f"INSERT INTO materias (nome, curso, {', '.join([f'materia{i + 1}' for i in range(6)])}) VALUES "
        comando_materias += f"('{self.nome_aluno}', '{self.curso_aluno}', '{nomes_materias[0]}', '{nomes_materias[1]}', '{nomes_materias[2]}', '{nomes_materias[3]}', '{nomes_materias[4]}', '{nomes_materias[5]}')"
        cursor.execute(comando_materias)
        conexao.commit()
        cursor.close()
        conexao.close()

        nova_conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_notas")
        novo_cursor = nova_conexao.cursor()
        comando_notas = ""

        for i, (nota1, nota2, nota3, nota4) in enumerate(val_matriz, start = 1):
            materia = nomes_materias[i - 1]
            comando_notas += f"('{self.nome_aluno}', '{self.curso_aluno}', '{materia}', '{nota1}', '{nota2}', '{nota3}', '{nota4}'), "
        comando_notas = comando_notas.rstrip(", ")
        novo_cursor.execute(f"INSERT INTO notas (nome, curso, materia, nota1, nota2, nota3, nota4) VALUES {comando_notas}")
        nova_conexao.commit()
        
        messagebox.showinfo(title = "Cadastro de notas", message = "Materias e Notas cadastradas com sucesso!")
        self.materia1.delete(0, 'end')
        self.materia2.delete(0, 'end')
        self.materia3.delete(0, 'end')
        self.materia4.delete(0, 'end')
        self.materia5.delete(0, 'end')
        self.materia6.delete(0, 'end')

        for i in range(1, 7):
            for j in range(1, 5):
                getattr(self, f"m{i}n{j}").delete(0, 'end')
        
        novo_cursor.close()
        nova_conexao.close()

class TelaGerarRelatorio():
    def __init__(self, janela):
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Relatório do Aluno")
        self.janela.geometry("700x700")
        self.janela.resizable(False, False)
        self.janela.transient(janela)
        self.janela.bind('<Return>', lambda event = None: self.pesquisar())

        self.frame_gerar_relatorio = ctk.CTkFrame(self.janela)
        
        self.cabecalho = ctk.CTkLabel(self.janela, text = "RELATÓRIO DE MATERIAS E NOTAS", font = ("verdana", 28), text_color = "blue")
        self.cabecalho.place(x = 100, y = 10)
        self.tipo_doc = ctk.CTkLabel(self.janela, text = "Tipo documento:", font = ("verdana", 16), justify = "center", width = 160, text_color = "blue")
        self.tipo_doc.place(x = 30, y = 60)
        self.comb_doc = ctk.CTkComboBox(self.janela, font = ("verdana", 16), justify = "center", width = 80, dropdown_fg_color = "white", dropdown_text_color = "blue", button_color = "green", values = ["RG", "CPF"])
        self.comb_doc.place(x = 190, y = 60)
        self.num_cpf = ctk.CTkLabel(self.janela, text = "Núm:", font = ("verdana", 16), text_color = "blue")
        self.num_cpf.place(x = 285, y = 60)
        self.numero_doc = ctk.CTkEntry(self.janela, placeholder_text = "Somente números", font = ("verdana", 16), justify = "center", width = 190)
        self.numero_doc.place(x = 345, y = 60)
        self.botao_pesquisar = ctk.CTkButton(self.janela, text = "Pesquisar", font = ("verdana", 16), width = 100, fg_color = "green", command = self.pesquisar)
        self.botao_pesquisar.place(x = 550, y = 60)
        self.nome = ctk.CTkLabel(self.janela, text = "", font = ("verdana", 16), justify = "center", width = 600)
        self.nome.place(x = 50, y = 110)
        self.curso = ctk.CTkLabel(self.janela, text = "", font = ("verdana", 16), justify = "center", width = 600)
        self.curso.place(x = 50, y = 160)
        self.botao_relatorio = ctk.CTkButton(self.janela, text = "Gerar Relatório", font = ("verdana", 16), height = 50, width = 200, fg_color = "red", command = self.gerar_relatorio)
        self.relatorio = ctk.CTkTextbox(self.janela, height = 300, width = 600, font = ("verdana", 16))
        self.botao_pdf = ctk.CTkButton(self.janela, text = "Exportar para PDF", font = ("verdana", 16), width = 200, fg_color = "blue", command = self.exportar_pdf)
        self.botao_pdf.place(x=475, y=630)
        self.botao_excel = ctk.CTkButton(self.janela, text = "Exportar para Excel", font = ("verdana", 16), width = 200, fg_color = "orange", command = self.exportar_excel)
        self.botao_excel.place(x=225, y=630)
        self.botao_voltar = ctk.CTkButton(self.janela, text = "Voltar", font = ("verdana", 16), fg_color = "green", width = 140, command = self.janela.destroy)
        self.botao_voltar.place(x = 30, y = 630)
        self.nome_aluno = ""
        self.curso_aluno = ""

    def pesquisar(self):
        if self.comb_doc.get() == "CPF" and not validacao_cpf(self.numero_doc.get()):
            messagebox.showerror(title = "Relatório de Notas", message = "CPF inválido. Por favor, insira um CPF válido.")
            return
        
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_alunos")
        cursor = conexao.cursor()
        consulta_aluno = f"SELECT nome, curso FROM aluno WHERE numerodoc = '{self.numero_doc.get()}'"
        cursor.execute(consulta_aluno)
        aluno_existente = cursor.fetchone()

        if not aluno_existente:
            messagebox.showerror(title = "Relatório de notas", message = "Aluno não encontrado com este número de documento.")
        else:
            self.nome_aluno = aluno_existente[0]
            self.curso_aluno = aluno_existente[1]
            self.nome.configure(text = f"{self.nome_aluno}", justify = "center", width = 600)
            self.curso.configure(text = f"{self.curso_aluno}", justify = "center", width = 600)
            self.botao_relatorio.place(x = 250, y = 210)
            self.relatorio.place(x = 50, y = 300)

    def calcular_media(self, notas):
        if all(isinstance(nota, (int, float)) for nota in notas):
            return sum(notas) / len(notas)
        return None

    def gerar_relatorio(self):
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_notas")
        cursor = conexao.cursor()
        consulta_notas = f"SELECT nome, curso, materia, nota1, nota2, nota3, nota4 FROM notas WHERE nome = '{self.nome_aluno}'"
        cursor.execute(consulta_notas)
        notas = cursor.fetchall()

        relatorio = ""
        for aluno, curso, materia, nota1, nota2, nota3, nota4 in notas:
            notas_materia = [nota1, nota2, nota3, nota4]
            media = self.calcular_media(notas_materia)

            if media is not None:
                situacao = "Aprovado" if media >= 6 else "Reprovado"
                relatorio += f"Aluno: {aluno}\nCurso: {curso}\nMatéria: {materia}\nMédia: {media:.2f}\nSituação: {situacao}\n\n"

        if relatorio:
            self.relatorio.delete("1.0", ctk.END)
            self.relatorio.insert(ctk.END, relatorio)
        else:
            messagebox.showinfo(title = "Relatório de Notas", message = "Nenhum registro encontrado.")

        cursor.close()
        conexao.close()

    def exportar_pdf(self):
        relatorio_texto = self.relatorio.get("1.0", ctk.END)

        if not relatorio_texto.isspace():
            nome_arquivo = "relatorio_notas.pdf"
            pdf = SimpleDocTemplate(nome_arquivo, pagesize=letter)
            styles = getSampleStyleSheet()
            style_title = styles["Title"]
            style_body = styles["BodyText"]
            elements = []
            title = Paragraph("Relatório de Notas", style_title)
            elements.append(title)
            body = Paragraph(relatorio_texto, style_body)
            elements.append(body)
            pdf.build(elements)
            messagebox.showinfo(title = "Exportação para PDF", message = f"Relatório exportado para {nome_arquivo}.")
        else:
            messagebox.showwarning(title = "Exportação para PDF", message = "Nenhum relatório para exportar.")

    def exportar_excel(self):
        relatorio_texto = self.relatorio.get("1.0", ctk.END)

        if not relatorio_texto.isspace():
            dados = [linha.split("\n") for linha in relatorio_texto.split("\n\n")]
            df = pd.DataFrame(dados, columns = ["Aluno", "Curso", "Matéria", "Média", "Situação"])
            nome_arquivo = "relatorio_notas.xlsx"
            df.to_excel(nome_arquivo, index=False)
            messagebox.showinfo(title = "Exportação para Excel", message = f"Relatório exportado para {nome_arquivo}.")
        else:
            messagebox.showwarning(title = "Exportação para Excel", message = "Nenhum relatório para exportar.")

class TelaExcluirAluno():
    def __init__(self, janela):
        self.janela = ctk.CTkToplevel(janela)
        self.janela.title("Exclusão de Aluno")
        self.janela.geometry("300x350")
        self.janela.resizable(False, False)
        self.janela.transient(janela)
        self.janela.bind('<Return>', lambda event = None: self.pesquisar())

        self.frame_excluir_aluno = ctk.CTkFrame(self.janela)

        self.cabecalho = ctk.CTkLabel(self.janela, text = "EXCLUIR ALUNO", font = ("verdana", 20), text_color = "blue")
        self.cabecalho.place(x = 70, y = 10)
        self.num_cpf = ctk.CTkLabel(self.janela, text = "Digite o CPF do aluno", font = ("verdana", 16))
        self.num_cpf.place(x = 65, y = 60)
        self.numero = ctk.CTkEntry(self.janela, placeholder_text = "Somente números", font = ("verdana", 16), justify = "center", width = 200)
        self.numero.place(x = 50, y = 100)
        self.botao_pesquisar = ctk.CTkButton(self.janela, text = "Pesquisar Aluno", font = ("verdana", 16), width = 120, fg_color = "green", command = self.pesquisar)
        self.botao_pesquisar.place(x = 80, y = 150)
        self.nome = ctk.CTkLabel(self.janela, text = "", font = ("verdana", 16), justify = "center", width = 250)
        self.nome.place(x = 5, y = 200)
        self.botao_confirmar = ctk.CTkButton(self.janela, text = "Confirmar Exclusão", font = ("verdana", 16), height = 50, width = 200, fg_color = "red", command = lambda: self.exclusao(self.numero.get()))
        self.botao_voltar = ctk.CTkButton(self.janela, text = "Voltar", font = ("verdana", 16), width = 150, command = self.janela.destroy)
        self.botao_voltar.place(x = 80, y = 310)

    def pesquisar(self):
        if not validacao_cpf(self.numero.get()):
            messagebox.showerror(title = "Exclusão de aluno", message = "CPF inválido. Por favor, insira um CPF válido.")
            return
        
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_alunos")
        cursor = conexao.cursor()
        consulta_aluno = f"SELECT nome FROM aluno WHERE numerodoc = '{self.numero.get()}'"
        cursor.execute(consulta_aluno)
        aluno_existente = cursor.fetchone()

        if not aluno_existente:
            messagebox.showerror(title = "Exclusão de aluno", message = "Aluno não encontrado com este número de documento.")
        else:
            nome = aluno_existente[0]
            self.nome.configure(text = f"{nome}", justify = "center", width = 250)
            self.botao_confirmar.configure(command = lambda: self.exclusao(self.numero.get()))
            self.botao_confirmar.place(x = 55, y = 240)

    def exclusao(self, munero_aluno):
        numero_aluno = self.numero.get()
        conexao = mc.connect(host = "localhost", user = "root", password = "3007", database = "cad_alunos")
        cursor = conexao.cursor()
        exclui_aluno = f"DELETE FROM aluno WHERE numerodoc = '{numero_aluno}'"
        cursor.execute(exclui_aluno)
        conexao.commit()
        messagebox.showinfo(title = "Exclusão  de aluno", message = "Aluno excluido com sucesso!")
        self.nome.configure(text = "")
        self.botao_confirmar.place_forget()
        self.numero.delete(0, 'end')
        cursor.close()
        conexao.close()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    TelaLogin(root)
    root.mainloop()

if __name__ == "__main__":
    main()