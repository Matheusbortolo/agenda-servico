import json
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry

class Agenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda para Prestadores de Serviço")
        self.root.state('zoomed')  # Abre maximizado
        
        self.clientes = []
        self.agendamentos = []
        self.carregar_dados()

        # Criar menu
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        
        menu_gerenciar = tk.Menu(menu_bar, tearoff=0)
        menu_gerenciar.add_command(label="Cadastrar Cliente", command=self.cadastrar_cliente)
        menu_gerenciar.add_command(label="Agendar Serviço", command=self.agendar_servico)
        menu_gerenciar.add_command(label="Visualizar Agendamentos", command=self.visualizar_agendamentos)
        menu_gerenciar.add_separator()
        menu_gerenciar.add_command(label="Sair", command=root.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_gerenciar)
        
        self.tree = ttk.Treeview(root, columns=("Cliente", "Serviço", "Data", "Valor"), show="headings")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Serviço", text="Serviço")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Valor", text="Valor (R$)")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.atualizar_listagem()

    def carregar_dados(self):
        try:
            with open("agenda.json", "r") as file:
                data = json.load(file)
                self.clientes = data.get("clientes", [])
                self.agendamentos = data.get("agendamentos", [])
        except FileNotFoundError:
            pass

    def salvar_dados(self):
        with open("agenda.json", "w") as file:
            json.dump({"clientes": self.clientes, "agendamentos": self.agendamentos}, file, indent=4)

    def cadastrar_cliente(self):
        def salvar_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            if nome and telefone:
                self.clientes.append({"nome": nome, "telefone": telefone})
                self.salvar_dados()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos!")
        
        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Cliente")
        tk.Label(janela, text="Nome:").pack()
        entry_nome = tk.Entry(janela)
        entry_nome.pack()
        tk.Label(janela, text="Telefone:").pack()
        entry_telefone = tk.Entry(janela)
        entry_telefone.pack()
        tk.Button(janela, text="Salvar", command=salvar_cliente).pack()
    
    def agendar_servico(self):
        def salvar_agendamento():
            nome = entry_nome.get()
            servico = entry_servico.get()
            data = cal.get_date() + " " + entry_hora.get()
            valor = entry_valor.get()
            
            if not any(c["nome"] == nome for c in self.clientes):
                messagebox.showerror("Erro", "Cliente não encontrado! Cadastre primeiro.")
                return
            
            try:
                datetime.strptime(data, "%d/%m/%Y %H:%M")
                valor = float(valor)
            except ValueError:
                messagebox.showerror("Erro", "Formato de data ou valor inválido!")
                return
            
            self.agendamentos.append({"cliente": nome, "servico": servico, "data": data, "valor": valor})
            self.salvar_dados()
            self.atualizar_listagem()
            messagebox.showinfo("Sucesso", "Serviço agendado com sucesso!")
            janela.destroy()
        
        janela = tk.Toplevel(self.root)
        janela.title("Agendar Serviço")
        tk.Label(janela, text="Nome do Cliente:").pack()
        entry_nome = tk.Entry(janela)
        entry_nome.pack()
        tk.Label(janela, text="Serviço:").pack()
        entry_servico = tk.Entry(janela)
        entry_servico.pack()
        tk.Label(janela, text="Data:").pack()
        cal = DateEntry(janela, date_pattern='dd/MM/yyyy')
        cal.pack()
        tk.Label(janela, text="Hora (HH:MM):").pack()
        entry_hora = tk.Entry(janela)
        entry_hora.pack()
        tk.Label(janela, text="Valor (R$):").pack()
        entry_valor = tk.Entry(janela)
        entry_valor.pack()
        tk.Button(janela, text="Salvar", command=salvar_agendamento).pack()
    
    def visualizar_agendamentos(self):
        self.atualizar_listagem()

    def atualizar_listagem(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for ag in self.agendamentos:
            self.tree.insert("", "end", values=(ag["cliente"], ag["servico"], ag["data"], f"R$ {ag['valor']:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = Agenda(root)
    root.mainloop()