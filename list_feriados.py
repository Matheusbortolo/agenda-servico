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

class FeriadosApp:
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

        # Configuração do Frame (contêiner) para a interface de Feriados
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Criação do Treeview para exibir os feriados
        self.tree = ttk.Treeview(self.frame, columns=("Nome", "Data Início", "Data Fim", "Flag Parar"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data Início", text="Data Início")
        self.tree.heading("Data Fim", text="Data Fim")
        self.tree.heading("Flag Parar", text="Flag Parar")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

        # Carregar os feriados assim que a tela for aberta
        self.carregar_feriados()

    def carregar_feriados(self):
        """Conectar ao banco de dados e carregar os feriados na interface."""
        self.db.connect()  # Conectar ao banco de dados
        print('Carregando feriados...')

        # Realizar a consulta SQL para pegar os feriados
        query = "SELECT nome, datahora_inicio, datahora_fim, flag_parar FROM feriados order by datahora_inicio"
        feriados = self.db.fetch_all(query)  # Buscando todos os resultados

        # Limpar a tabela antes de preencher novamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Verificando se existem feriados retornados e inserindo no Treeview
        if feriados:
            for feriado in feriados:
                # Formatar as datas antes de exibir
                data_inicio_formatada = self.formatar_data(feriado[1])  # Formatar datahora_inicio
                data_fim_formatada = self.formatar_data(feriado[2])  # Formatar datahora_fim
                self.tree.insert("", "end", values=(feriado[0], data_inicio_formatada, data_fim_formatada, feriado[3]))

        # Fechar a conexão com o banco de dados
        self.db.close()
