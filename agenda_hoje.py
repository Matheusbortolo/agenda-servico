import tkinter as tk
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from mysql_connection import MySQLConnection
from new_agendamento import CadastroAgendamentoApp  # Importando a classe de conexão
from request import APIRequest

load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

class ProximosAgendamentos:
    def __init__(self, root):
        self.root = root  # ✅ Usa a janela principal

        

        # Definir o dia atual
        self.current_day = datetime.today()

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#888888")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Criar botões de navegação
        self.nav_frame = tk.Frame(self.root, bg="#888888")
        self.nav_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(self.nav_frame, text="◀ Dia Anterior", command=self.prev_day)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.add_button = tk.Button(self.nav_frame, text="Novo Agendamento", command=lambda: CadastroAgendamentoApp(self.root))
        self.add_button.pack(padx=10, pady=5)
        

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
        
    def fetch_agendamentos(self):
        agora = datetime.now()
        # data_formatada = agora.strftime("%d/%m/%Y")
        data_formatada = self.current_day.strftime("%Y-%m-%d")

        # start_of_day = self.current_day.replace(hour=0, minute=0, second=0, microsecond=0)
        # end_of_day = self.current_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        api = APIRequest(
            base_url="http://127.0.0.1:8000",
            auth_url="http://127.0.0.1:8000/token/",
            username="matheus",
            password="senha123"
        )
        agendamentos = api.get(endpoint=f'/agenda/?datahora_inicio={data_formatada}&datahora_fim={data_formatada}')
        return agendamentos['message']

    def update_agenda(self):
        """Atualiza a tela com os agendamentos do dia atual."""
        # Limpar os agendamentos antigos
        for widget in self.agenda_frame.winfo_children():
            widget.destroy()

        # Buscar agendamentos do banco
        agendamentos = []
        agendamentos = self.fetch_agendamentos()

        # Exibir o dia atual
        self.date_label.config(text=f"Agendamentos de {self.current_day.strftime('%d/%m/%Y')}")

        # Adicionar os agendamentos como Labels
        if agendamentos:
            for agendamento in agendamentos:
                end_time = self.formatar_data( agendamento['datahora_fim'])  
                start_time =self.formatar_data( agendamento['datahora_inicio']) 
                endereco_agendamento = agendamento['endereco']
                descricao = agendamento['obs']
                email = agendamento['cliente']['email']
                endereco_cliente = agendamento['cliente']['endereco']
                cliente = agendamento['cliente']['nome']
                telefone = agendamento['cliente']['telefone']


                agendamento_label = tk.Label(
                    self.agenda_frame, 
                    text=f"Inicio:{start_time} - Fim:{end_time}: - Endereço Agendamento: {endereco_agendamento} - Descrição:{descricao} - Cliente:{cliente} - Email:{email}", 
                    font=("Arial", 12),  
                    bg="#888888",
                    anchor="w"
                )
                agendamento_label.pack(fill=tk.X, padx=5, pady=2)
        else:
            no_agenda_label = tk.Label(self.agenda_frame, text="Nenhum agendamento para hoje.", font=("Arial", 12), bg="#888888")
            no_agenda_label.pack(pady=10)

    def prev_day(self):
        """Voltar um dia."""
        self.current_day -= timedelta(days=1)
        self.update_agenda()

    def next_day(self):
        """Avançar um dia."""
        self.current_day += timedelta(days=1)
        self.update_agenda()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProximosAgendamentos(root)
    
    # Fechar conexão ao sair
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy()))

    root.mainloop()
