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

class ClientesApp:
    def destroy(self):
        """Método para destruir a janela de clientes."""
        self.frame.destroy()  # Fecha a janela de clientes
        
    def formatar_data(self, data_str):
        """Converte a string de data no formato 'YYYY-MM-DD HH:MM:SS' para o formato 'DD/MM/YYYY HH:MM'."""
        try:
            # data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
            data_formatada = data_str.strftime("%d/%m/%Y %H:%M")
            return data_formatada
        except Exception as e:
            print(f"Erro ao formatar data: {e}")
            return data_str  # Se falhar, retorna a data original

    def __init__(self, parent):
        self.parent = parent  # A janela principal (root)

        # Configuração do Frame (contêiner) para a interface de clientes
        self.frame = tk.Frame(self.parent, bg="#888888")  # Usando a cor cinza #888888
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal


        # Criação do Treeview para exibir os clientes
        self.tree = ttk.Treeview(self.frame, columns=("Nome", "Endereço", "Telefone", "E-mail"), show="headings")
        
        # Definir os cabeçalhos das colunas
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("E-mail", text="E-mail")
        
        # Alterando o estilo do Treeview
        style = ttk.Style()
        
        # Estilizar o Treeview
        style.configure("Treeview",
                        background="#888888",  # Cor de fundo das células
                        foreground="white",    # Cor do texto das células
                        fieldbackground="#888888")  # Cor de fundo das células

        # Estilizar os cabeçalhos
        style.configure("Treeview.Heading",
                        background="#888888",  # Cor de fundo do cabeçalho
                        foreground="white",    # Cor do texto no cabeçalho
                        font=("Arial", 10, "bold"))  # Alterar fonte do cabeçalho se necessário

        # Alterando a cor da linha selecionada
        style.map("Treeview",
                  background=[("selected", "#3c3c3c")],  # Cor de fundo da linha selecionada
                  foreground=[("selected", "white")])     # Cor do texto da linha selecionada
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

        # Carregar os clientes assim que a tela for aberta
        self.carregar_clientes()

    def carregar_clientes(self):
        """Conectar ao banco de dados e carregar os clientes na interface."""
        self.db.connect()  # Conectar ao banco de dados

        # Realizar a consulta SQL para pegar os clientes
        query = "SELECT nome, endereco, telefone, email FROM clientes"
        clientes = self.db.fetch_all(query)  # Buscando todos os resultados

        # Limpar a tabela antes de preencher novamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Verificando se existem clientes retornados e inserindo no Treeview
        if clientes:
            for cliente in clientes:
                self.tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3]))

        # Fechar a conexão com o banco de dados
        self.db.close()
