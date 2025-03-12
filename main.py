from dotenv import load_dotenv
from mysql_connection import MySQLConnection
from list_feriados import FeriadosApp 
from new_feriados import CadastroFeriadoApp 
from list_clientes import ClientesApp 
from new_cliente import CadastroClienteApp 
from list_tipos_servicos import TiposServicosApp 
from new_tipo_servico import NewTipoServicoApp 
from agenda import CalendarioSemanal 
from agenda_hoje import ProximosAgendamentos 

import os
import tkinter as tk

# Carregar variáveis de ambiente
load_dotenv()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão")
        self.root.configure(bg="#333333")  # Cor de fundo
        self.root.state("zoomed")  # Maximizar a janela
        
        self.conection()  # Conectar ao banco de dados

        # Criar o layout principal
        self.setup_ui()

    def conection(self):
        """Conectar ao banco de dados."""
        self.db = MySQLConnection(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def setup_ui(self):
        """Configuração da interface gráfica"""
        self.root.configure(bg="#333333")  # Cor de fundo

        # Criar um frame principal
        self.main_frame = tk.Frame(self.root, bg="#444444")
        self.main_frame.pack(fill="both", expand=True)

        # Criar um Canvas para o menu lateral
        self.canvas_menu = tk.Canvas(self.main_frame, width=250, bg="#222222", highlightthickness=0)
        self.canvas_menu.pack(side="left", fill="y")

        # Criar um frame dentro do Canvas para os botões
        self.menu_frame = tk.Frame(self.canvas_menu, bg="#222222")
        self.canvas_menu.create_window((125, 0), window=self.menu_frame, anchor="n")

        # Criar um frame para o conteúdo principal
        
        self.content_frame = tk.Frame(self.main_frame, bg="#888888")  # Alterado para vermelho escuro
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Adicionar os botões do menu lateral
        self.add_menu_buttons()

    def create_round_button(self, parent, text, command):
        """Cria um botão arredondado usando Canvas"""
        btn_canvas = tk.Canvas(parent, width=200, height=50, bg="#222222", highlightthickness=0)
        btn_canvas.pack(pady=5)

        # Criar um retângulo arredondado
        btn_canvas.create_oval(5, 5, 45, 45, fill="#444444", outline="#444444")  # Esquerda
        btn_canvas.create_oval(155, 5, 195, 45, fill="#444444", outline="#444444")  # Direita
        btn_canvas.create_rectangle(25, 5, 175, 45, fill="#444444", outline="#444444")  # Meio

        # Adicionar texto ao botão
        btn_canvas.create_text(100, 25, text=text, font=("Arial", 12, "bold"), fill="#FFFFFF")

        # Evento de clique
        btn_canvas.bind("<Button-1>", lambda event: command())

    def add_menu_buttons(self):
        """Cria botões no menu lateral"""
        self.create_round_button(self.menu_frame, "Listar Clientes", self.listar_cliente)
        self.create_round_button(self.menu_frame, "Novo Cliente", self.novo_cliente)

        self.create_round_button(self.menu_frame, "Listar Feriados", self.listar_feriado)
        self.create_round_button(self.menu_frame, "Novo Feriado", self.novo_feriado)

        self.create_round_button(self.menu_frame, "Listar Serviços", self.listar_tipo_servico)
        self.create_round_button(self.menu_frame, "Novo Serviço", self.novo_tipo_servico)

        self.create_round_button(self.menu_frame, "Calendário Semanal", self.agendamento)
        self.create_round_button(self.menu_frame, "Próximos Agendamentos", self.agendamento_hoje)

    def listar_cliente(self):
        self.load_content(ClientesApp)

    def novo_cliente(self):
        self.load_content(CadastroClienteApp)

    def listar_feriado(self):
        self.load_content(FeriadosApp)

    def novo_feriado(self):
        self.load_content(CadastroFeriadoApp)

    def listar_tipo_servico(self):
        self.load_content(TiposServicosApp)

    def novo_tipo_servico(self):
        self.load_content(NewTipoServicoApp)

    def agendamento(self):
        self.load_content(CalendarioSemanal)

    def agendamento_hoje(self):
        self.load_content(ProximosAgendamentos)

    def load_content(self, app_class):
        """Fecha telas anteriores e carrega uma nova tela"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        app_class(self.content_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
