import tkinter as tk
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
        self.root = root  # ✅ Usa a janela principal

        # Criar a instância de conexão com o banco de dados
        self.db = MySQLConnection(
            host=db_host, 
            user=db_user, 
            password=db_password, 
            database=db_name
        )
        
        # Inicializa a conexão com o banco
        self.db.connect()

        # Definir o dia atual
        self.current_day = datetime.today()

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#888888")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Criar botões de navegação
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(self.nav_frame, text="◀ Dia Anterior", command=self.prev_day)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.next_button = tk.Button(self.nav_frame, text="Próximo Dia ▶", command=self.next_day)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Label para mostrar o dia atual
        self.date_label = tk.Label(self.main_frame, text="", font=("Arial", 14, "bold"), bg="#888888")
        self.date_label.pack(pady=20)

        # Frame para os agendamentos
        self.agenda_frame = tk.Frame(self.main_frame, bg="#888888")
        self.agenda_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Atualizar a tela com os agendamentos do dia
        self.update_agenda()

    def fetch_agendamentos(self):
        """Busca os agendamentos do banco de dados para o dia atual."""
        query = """
            SELECT a.datahora_fim, a.datahora_inicio, a.endereco as endereco_agendamento, a.obs, c.email, c.endereco as endereco_cliente, c.nome, c.telefone
            FROM agendamentos a
            LEFT JOIN clientes c ON c.id = a.id_cliente
            WHERE datahora_inicio BETWEEN %s AND %s
            ORDER BY datahora_inicio
        """
        start_of_day = self.current_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = self.current_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        agendamentos = self.db.fetch_all(query, (start_of_day, end_of_day))
        return agendamentos if agendamentos else []

    def update_agenda(self):
        """Atualiza a tela com os agendamentos do dia atual."""
        # Limpar os agendamentos antigos
        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        # Buscar agendamentos do banco
        agendamentos = self.fetch_agendamentos()

        # Exibir o dia atual
        self.date_label.config(text=f"Agendamentos de {self.current_day.strftime('%d/%m/%Y')}")

        # Adicionar os agendamentos como Labels
        if agendamentos:
            for agendamento in agendamentos:



                end_time = agendamento[0].strftime('%H:%M')
                start_time = agendamento[1].strftime('%H:%M')
                endereco_agendamento = agendamento[2]
                descricao = agendamento[3]
                email = agendamento[4]
                endereco_cliente = agendamento[5]
                cliente = agendamento[6]
                telefone = agendamento[7]


                agendamento_label = tk.Label(
                    self.agenda_frame, 
                    text=f"Inicio:{start_time} - Fim:{end_time}: - Endereço Agendamento: {endereco_agendamento} - Descrição:{descricao} - Cliente:{cliente}", 
                    font=("Arial", 12),  
                    bg="#888888",
                    anchor="w"
                )
                agendamento_label.pack(fill=tk.X, padx=5, pady=2)
        else:
            no_agenda_label = tk.Label(self.agenda_frame, text="Nenhum agendamento para hoje.", font=("Arial", 12), bg="white")
            no_agenda_label.pack(pady=10)

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
