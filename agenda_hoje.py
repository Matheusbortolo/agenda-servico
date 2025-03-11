import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from mysql_connection import MySQLConnection  # Importando a classe de conexão

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

class ProximosAgendamentos:
    def __init__(self, root):
        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )

        self.root = root
        self.root.title("Próximos Agendamentos")
        self.root.geometry("600x400")

        # Inicializa a conexão com o banco
        self.db.connect()

        # Definir o dia atual
        self.current_day = datetime.today()

        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Criar botões de navegação
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(self.nav_frame, text="◀ Dia Anterior", command=self.prev_day)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.next_button = tk.Button(self.nav_frame, text="Próximo Dia ▶", command=self.next_day)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Label para mostrar o dia atual
        self.date_label = tk.Label(self.main_frame, text="", font=("Arial", 14, "bold"))
        self.date_label.pack(pady=20)

        # Lista de agendamentos
        self.agenda_listbox = tk.Listbox(self.main_frame, width=50, height=10)
        self.agenda_listbox.pack(pady=10)

        # Atualizar a tela com os agendamentos do dia
        self.update_agenda()

    def fetch_agendamentos(self):
        """Busca os agendamentos do banco de dados para o dia atual."""
        query = """
            SELECT datahora_inicio, datahora_fim, obs, a.endereco, c.nome, c.email, c.endereco, c.telefone
            FROM agendamentos a
            left join clientes c on c.id = a.id_cliente
            WHERE datahora_inicio BETWEEN %s AND %s
            ORDER BY datahora_inicio
        """
        start_of_day = self.current_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = self.current_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        agendamentos = self.db.fetch_all(query, (start_of_day, end_of_day))
        return agendamentos if agendamentos else []

    def update_agenda(self):
        """Atualiza a tela com os agendamentos do dia atual."""
        # Limpar a lista antes de atualizar
        self.agenda_listbox.delete(0, tk.END)

        # Buscar agendamentos do banco
        agendamentos = self.fetch_agendamentos()

        # Exibir o dia atual
        self.date_label.config(text=f"Agendamentos de {self.current_day.strftime('%d/%m/%Y')}")

        # Adicionar os agendamentos na lista
        if agendamentos:
            for agendamento in agendamentos:
                start_time = agendamento[0].strftime('%H:%M')
                end_time = agendamento[1].strftime('%H:%M')
                descricao = agendamento[2]
                cliente = agendamento[4]
                self.agenda_listbox.insert(tk.END, f"{start_time} - {end_time}: {descricao} - {cliente}")
        else:
            self.agenda_listbox.insert(tk.END, "Nenhum agendamento para hoje.")

    def prev_day(self):
        """Voltar um dia."""
        self.current_day -= timedelta(days=1)
        self.update_agenda()

    def next_day(self):
        """Avançar um dia."""
        self.current_day += timedelta(days=1)
        self.update_agenda()

    def close_db(self):
        """Fecha a conexão com o banco ao fechar o app."""
        self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProximosAgendamentos(root)
    
    # Fechar conexão ao sair
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close_db(), root.destroy()))

    root.mainloop()
