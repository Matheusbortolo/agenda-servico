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

class CadastroClienteApp:
    def destroy(self):
        """Método para destruir a janela de flientes."""
        self.frame.destroy()  # Fecha a janela de flientes

    def __init__(self, parent):
        self.parent = parent  # A janela principal (root)

        # Configuração do Frame (contêiner) para a interface de Cadastro de Clientes
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Faz o frame ocupar toda a área da janela principal

        # Título
        self.title_label = tk.Label(self.frame, text="Cadastro de Cliente", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Campos do formulário para cadastrar o fliente
        self.label_nome = tk.Label(self.frame, text="Nome do Cliente:")
        self.label_nome.pack(pady=5)
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.pack(pady=5)

        # Campos do formulário para cadastrar o fliente
        self.label_endereco = tk.Label(self.frame, text="Endereço:")
        self.label_endereco.pack(pady=5)
        self.entry_endereco = tk.Entry(self.frame)
        self.entry_endereco.pack(pady=5)

        # Campos do formulário para cadastrar o fliente
        self.label_telefone = tk.Label(self.frame, text="Telefone:")
        self.label_telefone.pack(pady=5)
        self.entry_telefone = tk.Entry(self.frame)
        self.entry_telefone.pack(pady=5)

        # Campos do formulário para cadastrar o fliente
        self.label_email = tk.Label(self.frame, text="E-mail:")
        self.label_email.pack(pady=5)
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.pack(pady=5)


        # Botão para cadastrar o fliente
        self.button_cadastrar = tk.Button(self.frame, text="Cadastrar Cliente", command=self.cadastrar_fliente)
        self.button_cadastrar.pack(pady=20)

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

    def cadastrar_fliente(self):
        """Função para inserir os dados de um novo fliente no banco de dados."""
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()


        # Validar se todos os campos foram preenchidos
        if not nome or not endereco or not telefone or email is None:
            messagebox.showwarning("Campos obrigatórios", "Todos os campos devem ser preenchidos.")
            return

        # Inserir o fliente no banco de dados
        try:
            self.db.connect()  # Conectar ao banco de dados

            # Query para inserir o novo fliente
            query = "INSERT INTO clientes (nome, endereco, telefone, email) VALUES (%s, %s, %s, %s)"
            params = (nome, endereco, telefone, email)
            self.db.execute_query(query, params)  # Executar o INSERT

            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

            # Limpar os campos após o cadastro
            self.entry_nome.delete(0, tk.END)
            self.entry_endereco.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")

        finally:
            # Fechar a conexão com o banco de dados
            self.db.close()
