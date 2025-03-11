import tkinter as tk
from tkinter import ttk
from mysql_connection import MySQLConnection  # Importando a classe de conexão MySQL
from dotenv import load_dotenv
from datetime import datetime

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
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Criação do Treeview para exibir os tipos_servico
        self.tree = ttk.Treeview(self.frame, columns=("Id", "Nome", "Obs"), show="headings")
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Obs", text="Obs")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

        # Carregar os tipos_servico assim que a tela for aberta
        self.carregar_tipos_servico()

    def carregar_tipos_servico(self):
        """Conectar ao banco de dados e carregar os tipos_servico na interface."""
        self.db.connect()  # Conectar ao banco de dados

        # Realizar a consulta SQL para pegar os tipos_servico
        query = "SELECT * FROM tipo_servico "
        tipos_servico = self.db.fetch_all(query)  # Buscando todos os resultados

        # Limpar a tabela antes de preencher novamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Verificando se existem tipos_servico retornados e inserindo no Treeview
        if tipos_servico:
            for feriado in tipos_servico:
                self.tree.insert("", "end", values=(feriado[0], feriado[1], feriado[2], ))

        # Fechar a conexão com o banco de dados
        self.db.close()
