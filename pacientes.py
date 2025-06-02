import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import conectar

def janela_pacientes():
    janela = tk.Toplevel()
    janela.title("Gerenciar Pacientes")
    janela.geometry("600x400")
    janela.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="#004d40", padding=6)
    style.configure("TLabel", font=("Helvetica", 10), background="#f5f5f5")
    style.configure("TEntry", padding=5)
    style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    def carregar_pacientes():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, nome, telefone FROM pacientes")
        pacientes = cur.fetchall()
        con.close()

        for row in tree.get_children():
            tree.delete(row)
        for paciente in pacientes:
            tree.insert('', 'end', values=paciente)

    def adicionar_paciente():
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO pacientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
        con.commit()
        con.close()
        carregar_pacientes()
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)

    def excluir_paciente():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um paciente para excluir.")
            return

        paciente_id = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir este paciente?")
        if confirm:
            con = conectar()
            cur = con.cursor()
            cur.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
            con.commit()
            con.close()
            carregar_pacientes()

    def editar_paciente():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um paciente para editar.")
            return

        paciente_id, nome_antigo, telefone_antigo = tree.item(selected)['values']
        novo_nome = entry_nome.get()
        novo_telefone = entry_telefone.get()

        if not novo_nome:
            messagebox.showwarning("Aviso", "Nome não pode estar vazio.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE pacientes SET nome = ?, telefone = ? WHERE id = ?", (novo_nome, novo_telefone, paciente_id))
        con.commit()
        con.close()
        carregar_pacientes()
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)

    def preencher_campos(event):
        selected = tree.focus()
        if not selected:
            return
        paciente_id, nome, telefone = tree.item(selected)['values']
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, nome)
        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, telefone)

    # Frame superior com formulário
    frame_form = ttk.Frame(janela, padding=10)
    frame_form.pack(fill=tk.X)

    ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
    entry_nome = ttk.Entry(frame_form, width=30)
    entry_nome.grid(row=0, column=1, pady=2, padx=5)

    ttk.Label(frame_form, text="Telefone:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_telefone = ttk.Entry(frame_form, width=30)
    entry_telefone.grid(row=1, column=1, pady=2, padx=5)

    ttk.Button(frame_form, text="Adicionar", command=adicionar_paciente).grid(row=2, column=0, pady=10)
    ttk.Button(frame_form, text="Editar", command=editar_paciente).grid(row=2, column=1, pady=10, sticky=tk.W)
    ttk.Button(frame_form, text="Excluir", command=excluir_paciente).grid(row=2, column=1, pady=10, sticky=tk.E)

    # Tabela de pacientes
    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Telefone"), show='headings')
    for col in ("ID", "Nome", "Telefone"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    carregar_pacientes()
