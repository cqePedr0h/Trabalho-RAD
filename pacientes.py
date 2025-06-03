import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import conectar

def janela_pacientes():
    janela = tk.Toplevel()
    janela.title("Gerenciar Pacientes")
    janela.geometry("800x500")
    janela.configure(bg="#f7f6f2")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    frame_principal = ttk.Frame(janela, padding=20)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Labels com fonte maior
    ttk.Label(frame_principal, text="Nome:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Idade:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Telefone:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Email:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=6)

    # Entradas maiores e com fonte maior
    nome_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    nome_entry.grid(row=0, column=1, pady=6)

    idade_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    idade_entry.grid(row=1, column=1, pady=6)

    telefone_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    telefone_entry.grid(row=2, column=1, pady=6)

    email_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    email_entry.grid(row=3, column=1, pady=6)

    # Treeview
    tree = ttk.Treeview(frame_principal, columns=("ID", "Nome", "Idade", "Telefone", "Email"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    frame_principal.grid_rowconfigure(5, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)

    def carregar_pacientes():
        for row in tree.get_children():
            tree.delete(row)
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM pacientes")
        for paciente in cur.fetchall():
            tree.insert('', tk.END, values=paciente)
        con.close()

    def adicionar_paciente():
        nome = nome_entry.get()
        idade = idade_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()

        if not nome:
            messagebox.showwarning("Atenção", "O campo nome é obrigatório.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO pacientes (nome, idade, telefone, email) VALUES (?, ?, ?, ?)",
                    (nome, idade, telefone, email))
        con.commit()
        con.close()
        carregar_pacientes()
        limpar_campos()

    def excluir_paciente():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para excluir.")
            return

        paciente_id = tree.item(selecionado)["values"][0]
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este paciente?"):
            con = conectar()
            cur = con.cursor()
            cur.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
            con.commit()
            con.close()
            carregar_pacientes()

    def editar_paciente():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para editar.")
            return

        paciente_id = tree.item(selecionado)["values"][0]
        nome = nome_entry.get()
        idade = idade_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE pacientes
            SET nome = ?, idade = ?, telefone = ?, email = ?
            WHERE id = ?
        """, (nome, idade, telefone, email, paciente_id))
        con.commit()
        con.close()
        carregar_pacientes()
        limpar_campos()

    def preencher_campos(event):
        selecionado = tree.focus()
        if not selecionado:
            return
        dados = tree.item(selecionado)["values"]
        nome_entry.delete(0, tk.END)
        idade_entry.delete(0, tk.END)
        telefone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

        nome_entry.insert(0, dados[1])
        idade_entry.insert(0, dados[2])
        telefone_entry.insert(0, dados[3])
        email_entry.insert(0, dados[4])

    def limpar_campos():
        nome_entry.delete(0, tk.END)
        idade_entry.delete(0, tk.END)
        telefone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", preencher_campos)

    frame_botoes = ttk.Frame(frame_principal)
    frame_botoes.grid(row=4, column=0, columnspan=3, pady=10)

    ttk.Button(frame_botoes, text="Adicionar", command=adicionar_paciente).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botoes, text="Editar", command=editar_paciente).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botoes, text="Excluir", command=excluir_paciente).grid(row=0, column=2, padx=5)

    carregar_pacientes()
