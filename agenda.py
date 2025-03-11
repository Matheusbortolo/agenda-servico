import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from  new_agendamento import CadastroAgendamentoApp

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from mysql_connection import MySQLConnection  # Importando a classe de conexão


class CalendarioSemanal:
    def destroy(self):
        """Método para destruir a janela de flientes."""        
        self.nav_frame.destroy()  # Fecha a janela de flientes
        self.main_frame.destroy()  # Fecha a janela de flientes

    def __init__(self, root):
        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

        self.root = root
        self.root.title("Agenda Semanal")
        self.root.geometry("1000x600")

        self.current_week_start = datetime.today() - timedelta(days=datetime.today().weekday())  # Segunda-feira da semana atual

        # Inicializa a conexão com o banco
        self.db.connect()

        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Criar Canvas para rolagem
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem
        self.scrollbar_y = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Frame interno dentro do Canvas
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Criar botões de navegação
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(self.nav_frame, text="◀ Semana Anterior", command=self.prev_week)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.add_button = tk.Button(self.nav_frame, text="Novo Agendamento", command=lambda: CadastroAgendamentoApp(self.root))
        self.add_button.pack(padx=10, pady=5)
        
        self.next_button = tk.Button(self.nav_frame, text="Próxima Semana ▶", command=self.next_week)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Criar grade da agenda
        self.create_schedule()

        # Atualizar eventos da semana atual
        self.update_schedule()

    def create_schedule(self):
        """Cria o grid da agenda com horários e dias da semana."""
        self.days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        self.hours = [f"{hora}:00" for hora in range(7, 20)]  # 07:00 às 19:00

        # Criar cabeçalhos das colunas (dias da semana)
        for col, dia in enumerate(self.days):
            label = tk.Label(self.content_frame, text=dia, font=("Arial", 12, "bold"), bg="lightgray", borderwidth=1, relief="solid")
            label.grid(row=0, column=col+1, sticky="nsew", padx=1, pady=1)

        # Criar a primeira coluna (horários)
        for row, horario in enumerate(self.hours):
            label = tk.Label(self.content_frame, text=horario, font=("Arial", 10), bg="white", borderwidth=1, relief="solid")
            label.grid(row=row+1, column=0, sticky="nsew", padx=1, pady=1)

        # Criar células para cada dia e horário
        self.cells = []
        for row in range(len(self.hours)):
            row_cells = []
            for col in range(len(self.days)):
                cell = tk.Label(self.content_frame, text="", bg="white", borderwidth=1, relief="solid")
                cell.grid(row=row+1, column=col+1, sticky="nsew", padx=1, pady=1)
                row_cells.append(cell)
            self.cells.append(row_cells)

        # Ajustar responsividade
        for i in range(len(self.days) + 1):
            self.content_frame.columnconfigure(i, weight=1)
        for i in range(len(self.hours) + 1):
            self.content_frame.rowconfigure(i, weight=1)

    def fetch_events(self):
        """Busca os agendamentos do banco de dados para a semana atual."""
        week_end = self.current_week_start + timedelta(days=6)
        query = """
            SELECT datahora_inicio, datahora_fim 
            FROM agendamentos 
            WHERE datahora_inicio BETWEEN %s AND %s
        """
        events = self.db.fetch_all(query, (self.current_week_start, week_end))
        return events if events else []

    def update_schedule(self):
        """Atualiza a agenda com os eventos da semana atual."""
        # Limpar células antes de adicionar eventos
        for row in range(len(self.hours)):
            for col in range(len(self.days)):
                self.cells[row][col].config(text="", bg="white")

        # Buscar eventos do banco
        events = self.fetch_events()

        for event in events:
            start_time = event[0]
            end_time = event[1]

            # Definir o dia e hora do evento
            day_offset = start_time.weekday()  # Segunda = 0, Terça = 1, etc.
            hour_offset = start_time.hour - 7  # Ajustar para começar das 07:00

            if 0 <= day_offset < 7 and 0 <= hour_offset < len(self.hours):
                event_text = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                self.cells[hour_offset][day_offset].config(text=event_text, bg="lightblue")

        # Atualizar título da janela com a data da semana
        self.root.title(f"Agenda Semanal ({self.current_week_start.strftime('%d/%m/%Y')} - {(self.current_week_start + timedelta(days=6)).strftime('%d/%m/%Y')})")
        

        # Ajustar rolagem
        self.content_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def prev_week(self):
        """Voltar uma semana."""
        self.current_week_start -= timedelta(days=7)
        self.update_schedule()

    def next_week(self):
        """Avançar uma semana."""
        self.current_week_start += timedelta(days=7)
        self.update_schedule()

    def close_db(self):
        """Fecha a conexão com o banco ao fechar o app."""
        self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    
    # Fechar conexão ao sair
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close_db(), root.destroy()))

    root.mainloop()
