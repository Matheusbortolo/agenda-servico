import tkinter as tk
from tkinter import ttk, messagebox
from mysql_connection import MySQLConnection  # Importando a classe de conexão MySQL
from dotenv import load_dotenv
from datetime import datetime
import os
from tkcalendar import DateEntry  # Importando o DateEntry
from tkinter import StringVar

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

class CadastroFeriadoApp:
    def __init__(self, parent):
        self.parent = parent  # A janela principal (root)

        # Configuração do Frame (contêiner) para a interface de Cadastro de Feriados
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Título
        self.title_label = tk.Label(self.frame, text="Cadastro de Feriado", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Campos do formulário para cadastrar o feriado
        self.label_nome = tk.Label(self.frame, text="Nome do Feriado:")
        self.label_nome.pack(pady=5)
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.pack(pady=5)

        self.label_data_inicio = tk.Label(self.frame, text="Data Início:")
        self.label_data_inicio.pack(pady=5)
        self.data_inicio = StringVar()
        self.entry_data_inicio = DateEntry(self.frame, textvariable=self.data_inicio, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_data_inicio.pack(pady=5)

        self.label_hora_inicio = tk.Label(self.frame, text="Hora Início:")
        self.label_hora_inicio.pack(pady=5)
        self.entry_hora_inicio = ttk.Combobox(self.frame, values=[f'{i:02d}:{j:02d}' for i in range(24) for j in range(0, 60, 5)], state="readonly")
        self.entry_hora_inicio.set('00:00')  # Definindo um valor inicial
        self.entry_hora_inicio.pack(pady=5)

        self.label_data_fim = tk.Label(self.frame, text="Data Fim:")
        self.label_data_fim.pack(pady=5)
        self.data_fim = StringVar()
        self.entry_data_fim = DateEntry(self.frame, textvariable=self.data_fim, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_data_fim.pack(pady=5)

        self.label_hora_fim = tk.Label(self.frame, text="Hora Fim:")
        self.label_hora_fim.pack(pady=5)
        self.entry_hora_fim = ttk.Combobox(self.frame, values=[f'{i:02d}:{j:02d}' for i in range(24) for j in range(0, 60, 5)], state="readonly")
        self.entry_hora_fim.set('00:00')  # Definindo um valor inicial
        self.entry_hora_fim.pack(pady=5)

        # Alterado para ComboBox com "Sim" ou "Não"
        self.label_flag_parar = tk.Label(self.frame, text="Flag Parar (Sim ou Não):")
        self.label_flag_parar.pack(pady=5)
        self.entry_flag_parar = ttk.Combobox(self.frame, values=["Sim", "Não"], state="readonly")
        self.entry_flag_parar.set("Não")  # Definindo um valor inicial
        self.entry_flag_parar.pack(pady=5)

        # Botão para cadastrar o feriado
        self.button_cadastrar = tk.Button(self.frame, text="Cadastrar Feriado", command=self.cadastrar_feriado)
        self.button_cadastrar.pack(pady=20)

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

    def cadastrar_feriado(self):
        """Função para inserir os dados de um novo feriado no banco de dados."""
        nome = self.entry_nome.get()
        data_inicio = f"{self.data_inicio.get()} {self.entry_hora_inicio.get()}"
        data_fim = f"{self.data_fim.get()} {self.entry_hora_fim.get()}"
        
        # Converter "Sim" para 1 e "Não" para 0
        flag_parar = 1 if self.entry_flag_parar.get() == "Sim" else 0

        # Validar se todos os campos foram preenchidos
        if not nome or not data_inicio or not data_fim or flag_parar is None:
            messagebox.showwarning("Campos obrigatórios", "Todos os campos devem ser preenchidos.")
            return

        # Inserir o feriado no banco de dados
        try:
            self.db.connect()  # Conectar ao banco de dados

            # Query para inserir o novo feriado
            query = "INSERT INTO feriados (nome, datahora_inicio, datahora_fim, flag_parar) VALUES (%s, %s, %s, %s)"
            params = (nome, data_inicio, data_fim, flag_parar)
            self.db.execute_query(query, params)  # Executar o INSERT

            messagebox.showinfo("Sucesso", "Feriado cadastrado com sucesso!")

            # Limpar os campos após o cadastro
            self.entry_nome.delete(0, tk.END)
            self.entry_flag_parar.set("Não")  # Resetando para o valor inicial
            self.data_inicio.set('')
            self.entry_hora_inicio.set('00:00')
            self.data_fim.set('')
            self.entry_hora_fim.set('00:00')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar feriado: {e}")

        finally:
            # Fechar a conexão com o banco de dados
            self.db.close()
