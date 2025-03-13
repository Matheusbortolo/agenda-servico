import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from mysql_connection import MySQLConnection  # Classe de conexão
import os
from request import APIRequest


api = APIRequest(
    base_url="http://127.0.0.1:8000",
    auth_url="http://127.0.0.1:8000/token/",
    username="matheus",
    password="senha123"
)
class CadastroAgendamentoApp:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)  # Criando uma nova janela separada
        self.window.title("Novo Agendamento")
        self.window.geometry("400x400")


        # Criando os campos da tela
        tk.Label(self.window, text="Data/Hora Início:").pack(pady=2)
        self.datahora_inicio = DateEntry(self.window, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.datahora_inicio.pack(pady=2)
        self.hora_inicio = ttk.Combobox(self.window, values=[f"{h:02}:00" for h in range(7, 20)])
        self.hora_inicio.pack(pady=2)

        tk.Label(self.window, text="Data/Hora Fim:").pack(pady=2)
        self.datahora_fim = DateEntry(self.window, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.datahora_fim.pack(pady=2)
        self.hora_fim = ttk.Combobox(self.window, values=[f"{h:02}:00" for h in range(7, 20)])
        self.hora_fim.pack(pady=2)

        tk.Label(self.window, text="Serviço:").pack(pady=2)
        self.id_servico = ttk.Combobox(self.window)
        self.id_servico.pack(pady=2)

        tk.Label(self.window, text="Cliente:").pack(pady=2)
        self.id_cliente = ttk.Combobox(self.window)
        self.id_cliente.pack(pady=2)

        tk.Label(self.window, text="Endereço:").pack(pady=2)
        self.endereco = tk.Entry(self.window, width=40)
        self.endereco.pack(pady=2)

        tk.Label(self.window, text="Observação:").pack(pady=2)
        self.obs = tk.Entry(self.window, width=40)
        self.obs.pack(pady=2)

        self.carregar_comboboxes()

        tk.Button(self.window, text="Salvar", command=self.salvar_agendamento).pack(pady=10)

        # Fechar conexão ao fechar a janela
        self.window.protocol("WM_DELETE_WINDOW", self.close_db)

    def carregar_comboboxes(self):

        """Carrega os valores para as comboboxes de serviços e clientes do banco de dados."""
        servicos = api.get(endpoint='/tipo-servico/')
        self.id_servico["values"] = [f"{s['id']} - {s['nome']}" for s in servicos['message']]

        clientes = api.get(endpoint='/clientes/')
        self.id_cliente["values"] = [f"{c['id']} - {c['nome']}" for c in clientes['message']]

    def salvar_agendamento(self):
        """Salva o novo agendamento no banco de dados."""
        try:
            # Formatar data e hora
            inicio = f"{self.datahora_inicio.get()} {self.hora_inicio.get()}:00"
            fim = f"{self.datahora_fim.get()} {self.hora_fim.get()}:00"

            id_servico = self.id_servico.get().split(" - ")[0]
            id_cliente = self.id_cliente.get().split(" - ")[0]
            endereco = self.endereco.get()
            obs = self.obs.get()


            # feriados = api.get(endpoint='/feriados/')
            agenda = {"datahora_inicio":inicio,"datahora_fim":fim,"id_servico":id_servico,"obs":obs,"endereco":endereco,"id_cliente":id_cliente}
            res = api.post(endpoint='/agenda/', data=agenda)
            print(res)
            
            messagebox.showinfo("Sucesso", "Agendamento salvo com sucesso!")
            self.window.destroy()  # Fecha a janela após salvar
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def close_db(self):
        """Fecha a conexão com o banco ao sair."""
        self.window.destroy()

# Criar uma função para abrir a tela em uma nova janela
def abrir_cadastro_agendamento(parent):
    CadastroAgendamentoApp(parent)

# Exemplo de uso: abrir a tela a partir do menu principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("App Principal")
    root.geometry("300x200")

    tk.Button(root, text="Novo Agendamento", command=lambda: abrir_cadastro_agendamento(root)).pack(pady=20)

    root.mainloop()
