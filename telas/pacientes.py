import tkinter as tk
from tkinter import ttk, messagebox
from criar_tabelas import conectar


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

    ttk.Label(frame_principal, text="Nome:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Data de Nascimento (DD/MM/AAAA):", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Telefone:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame_principal, text="Email:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=6)

    nome_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    nome_entry.grid(row=0, column=1, pady=6)

    def mascara_data(event):
        texto = nascimento_entry.get().replace("/", "")[:8]
        novo = ""
        for i in range(len(texto)):
            if i in [2, 4]:
                novo += "/"
            novo += texto[i]
        nascimento_entry.delete(0, tk.END)
        nascimento_entry.insert(0, novo)

    nascimento_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    nascimento_entry.grid(row=1, column=1, pady=6)
    nascimento_entry.bind("<KeyRelease>", mascara_data)

    telefone_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    telefone_entry.grid(row=2, column=1, pady=6)

    email_entry = ttk.Entry(frame_principal, width=50, font=("Segoe UI", 12))
    email_entry.grid(row=3, column=1, pady=6)

    tree = ttk.Treeview(frame_principal, columns=("ID", "Nome", "Nascimento", "Telefone", "Email"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    frame_principal.grid_rowconfigure(5, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)

    def carregar_pacientes():
        for row in tree.get_children():
            tree.delete(row)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM paciente")
        for paciente in cur.fetchall():
            tree.insert('', tk.END, values=paciente)
        conn.close()

    def adicionar_paciente():
        nome = nome_entry.get()
        nascimento = nascimento_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()

        if not nome or not telefone or not email:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (Nome, Telefone, Email).")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO paciente (nome, data_nascimento, telefone, email) VALUES (?, ?, ?, ?)",
                    (nome, nascimento, telefone, email))
        conn.commit()
        conn.close()
        carregar_pacientes()
        limpar_campos()

    def excluir_paciente():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para excluir.")
            return
        paciente_id = tree.item(selecionado)["values"][0]
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este paciente?"):
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM paciente WHERE id = ?", (paciente_id,))
            conn.commit()
            conn.close()
            carregar_pacientes()

    def editar_paciente():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para editar.")
            return
        paciente_id = tree.item(selecionado)["values"][0]
        nome = nome_entry.get()
        nascimento = nascimento_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()

        if not nome or not telefone or not email:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (Nome, Telefone, Email).")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE paciente
            SET nome = ?, data_nascimento = ?, telefone = ?, email = ?
            WHERE id = ?
        """, (nome, nascimento, telefone, email, paciente_id))
        conn.commit()
        conn.close()
        carregar_pacientes()
        limpar_campos()

    def selecionar_item(event):
        selecionado = tree.focus()
        if selecionado:
            valores = tree.item(selecionado)["values"]
            nome_entry.delete(0, tk.END)
            nome_entry.insert(0, valores[1])
            nascimento_entry.delete(0, tk.END)
            nascimento_entry.insert(0, valores[2])
            telefone_entry.delete(0, tk.END)
            telefone_entry.insert(0, valores[3])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, valores[4])

    def limpar_campos():
        nome_entry.delete(0, tk.END)
        nascimento_entry.delete(0, tk.END)
        telefone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", selecionar_item)

    btn_frame = ttk.Frame(frame_principal)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Adicionar", command=adicionar_paciente).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Editar", command=editar_paciente).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Excluir", command=excluir_paciente).grid(row=0, column=2, padx=5)

    carregar_pacientes()
