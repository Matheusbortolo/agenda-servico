import tkinter as tk
from tkinter import ttk
from mysql_connection import MySQLConnection  # Importando a classe de conexão MySQL
from dotenv import load_dotenv
from datetime import datetime
from request import APIRequest

import os

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

class TiposServicosApp:
    def destroy(self):
        self.frame.destroy()  # Fecha a janela de tipos_servico
        
    def __init__(self, parent):
        self.parent = parent  # A janela principal (root)

        # Configuração do Frame (contêiner) para a interface de TiposServicos
        self.frame = tk.Frame(self.parent, bg="#888888")
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Criação do Treeview para exibir os tipos_servico
        self.tree = ttk.Treeview(self.frame, columns=("Id", "Nome", "Obs"), show="headings")
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Obs", text="Obs")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Carregar os tipos_servico assim que a tela for aberta
        self.carregar_tipos_servico()

    def carregar_tipos_servico(self):
        api = APIRequest(
            base_url="http://127.0.0.1:8000",
            auth_url="http://127.0.0.1:8000/token/",
            username="matheus",
            password="senha123"
        )
        tipos_servico = api.get(endpoint='/tipo-servico/')
        print(tipos_servico)
        # Limpar a tabela antes de preencher novamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Verificando se existem tipos_servico retornados e inserindo no Treeview
        if tipos_servico['message']:
            for feriado in tipos_servico['message']:
                self.tree.insert("", "end", values=(feriado['id'], feriado['nome'], feriado['obs'], ))

