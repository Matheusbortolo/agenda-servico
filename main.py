from dotenv import load_dotenv 
from mysql_connection import MySQLConnection
from tkinter import Menu
from list_feriados import FeriadosApp 
from new_feriados import CadastroFeriadoApp 

import os
import tkinter as tk
from tkinter import ttk, messagebox

# Carregar variáveis de ambiente
load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão")
        self.feriados_app = None  # Variável para armazenar a instância da tela de Feriados
        self.cadastro_feriados_app = None  # Variável para armazenar a instância da tela de Feriados
        
        self.conection()  # Conectar ao banco de dados

        # Maximizar a janela
        self.root.state("zoomed")

        # Criação do menu principal
        self.menu_bar = Menu(self.root)

        # Menu Cliente
        cliente_menu = Menu(self.menu_bar, tearoff=0)
        cliente_menu.add_command(label="Listar Clientes", command=self.listar_cliente)
        cliente_menu.add_command(label="Novo Cliente", command=self.novo_cliente)
        self.menu_bar.add_cascade(label="Cliente", menu=cliente_menu)

        # Menu Feriado
        feriado_menu = Menu(self.menu_bar, tearoff=0)
        feriado_menu.add_command(label="Listar Feriados", command=self.listar_feriado)
        feriado_menu.add_command(label="Novo Feriado", command=self.novo_feriado)
        self.menu_bar.add_cascade(label="Feriado", menu=feriado_menu)

        # Menu Tipo Serviço
        tipo_servico_menu = Menu(self.menu_bar, tearoff=0)
        tipo_servico_menu.add_command(label="Listar Tipos de Serviço", command=self.listar_tipo_servico)
        tipo_servico_menu.add_command(label="Novo Tipo de Serviço", command=self.novo_tipo_servico)
        self.menu_bar.add_cascade(label="Tipo Serviço", menu=tipo_servico_menu)

        # Menu Agendamento
        self.menu_bar.add_command(label="Agendamento", command=self.agendamento)

        # Definir o menu na janela
        self.root.config(menu=self.menu_bar)

    def conection(self):
        """Conectar ao banco de dados."""
        self.db = MySQLConnection(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def listar_cliente(self):
        print("Abrir Listar Clientes")

    def novo_cliente(self):
        print("Abrir Novo Cliente")

    def listar_feriado(self):
        """Verificar se a tela de feriados já está aberta, e caso contrário, abrir"""
        print("Abrir Listar Feriados")
        if not hasattr(self, 'feriados_app') or self.feriados_app is None:
            # Criar a instância da tela de feriados
            self.feriados_app = FeriadosApp(self.root)
        else:
            print("Tela de feriados já está aberta!")

    def novo_feriado(self):
        """Verificar se a tela de cadastro de feriado já está aberta, e caso contrário, abrir"""
        print("Abrir Novo Feriado")
        if not hasattr(self, 'cadastro_feriados_app') or self.cadastro_feriados_app is None:
            # Criar a instância da tela de cadastro de feriados
            self.cadastro_feriados_app = CadastroFeriadoApp(self.root)
        else:
            print("Tela de cadastro de feriados já está aberta!")

    def listar_tipo_servico(self):
        print("Abrir Listar Tipos de Serviço")

    def novo_tipo_servico(self):
        print("Abrir Novo Tipo de Serviço")

    def agendamento(self):
        print("Abrir Agendamento")


if __name__ == "__main__":
    root = tk.Tk()  # Criando a janela principal
    app = MainApp(root)  # Inicializando a classe da interface principal
    root.mainloop()  # Iniciar o loop da interface gráfica
