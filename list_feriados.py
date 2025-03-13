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

class FeriadosApp:
    def destroy(self):
        """Método para destruir a janela de feriados."""
        self.frame.destroy()  # Fecha a janela de feriados
        
        
    def formatar_data(self, data_str: str) -> str:
        """
        Converte uma string de data para um objeto datetime e formata no padrão brasileiro (DD/MM/YYYY HH:MM).
        """
        try:
            # Detecta automaticamente o formato da data
            formatos = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"]
            
            for formato in formatos:
                try:
                    data_obj = datetime.strptime(data_str, formato)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError("Formato de data não reconhecido.")

            # Retorna a data formatada no padrão brasileiro
            return data_obj.strftime("%d/%m/%Y %H:%M")

        except Exception as e:
            return f"Erro ao converter data: {e}"
        
    def __init__(self, parent):
        self.parent = parent  # A janela principal (root)

        # Configuração do Frame (contêiner) para a interface de Feriados
        self.frame = tk.Frame(self.parent, bg="#888888")
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Criação do Treeview para exibir os feriados
        self.tree = ttk.Treeview(self.frame, columns=("Nome", "Data Início", "Data Fim", "Flag Parar"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data Início", text="Data Início")
        self.tree.heading("Data Fim", text="Data Fim")
        self.tree.heading("Flag Parar", text="Flag Parar")
        self.tree.pack(fill=tk.BOTH, expand=True)


        # Carregar os feriados assim que a tela for aberta
        self.carregar_feriados()

    def carregar_feriados(self):
        api = APIRequest(
            base_url="http://127.0.0.1:8000",
            auth_url="http://127.0.0.1:8000/token/",
            username="matheus",
            password="senha123"
        )
        feriados = api.get(endpoint='/feriados/')

        # Limpar a tabela antes de preencher novamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Verificando se existem feriados retornados e inserindo no Treeview
        if feriados['message']:
            for feriado in feriados['message']:
                # Formatar as datas antes de exibir
                data_inicio_formatada = self.formatar_data(feriado['datahora_inicio'])  # Formatar datahora_inicio
                data_fim_formatada = self.formatar_data(feriado['datahora_fim'])  # Formatar datahora_fim
                parar = 'Não'
                if feriado['flag_parar']:
                    parar = 'Sim'
                self.tree.insert("", "end", values=(feriado['nome'], data_inicio_formatada, data_fim_formatada, parar))
