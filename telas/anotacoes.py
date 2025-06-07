import tkinter as tk
from tkinter import ttk, messagebox
from criar_tabelas import conectar
from datetime import datetime

def janela_anotacoes():
    janela = tk.Toplevel()
    janela.title("Gerenciar Anotações")
    janela.geometry("800x550")
    janela.configure(bg="#f7f6f2")
    janela.iconbitmap("logos/favicon.ico")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    frame_principal = ttk.Frame(janela, padding=20)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame_principal, text="Paciente:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5)
    ttk.Label(frame_principal, text="Data (DD/MM/AAAA):", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=5)
    ttk.Label(frame_principal, text="Conteúdo:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="nw", pady=5)

    paciente_combobox = ttk.Combobox(frame_principal, font=("Segoe UI", 12), width=40)
    paciente_combobox.grid(row=0, column=1, sticky="ew", pady=5)

    def carregar_pacientes():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM paciente")
        pacientes = cur.fetchall()
        conn.close()
        paciente_combobox["values"] = [f"{id_} - {nome}" for id_, nome in pacientes]

    carregar_pacientes()

    def mascara_data(event):
        texto = data_entry.get().replace("/", "")[:8]
        novo = ""
        for i in range(len(texto)):
            if i in [2, 4]:
                novo += "/"
            novo += texto[i]
        data_entry.delete(0, tk.END)
        data_entry.insert(0, novo)

    data_entry = ttk.Entry(frame_principal, font=("Segoe UI", 12))
    data_entry.grid(row=1, column=1, sticky="ew", pady=5)
    data_entry.bind("<KeyRelease>", mascara_data)

    conteudo_text = tk.Text(frame_principal, height=5, font=("Segoe UI", 12))
    conteudo_text.grid(row=2, column=1, sticky="ew", pady=5)

    frame_principal.grid_columnconfigure(1, weight=1)

    tree = ttk.Treeview(frame_principal, columns=("ID", "Paciente", "Data", "Conteúdo"), show="headings")
    for col, w in zip(("ID", "Paciente", "Data", "Conteúdo"), (50, 150, 100, 400)):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="w")
    tree.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

    frame_principal.grid_rowconfigure(3, weight=1)

    def carregar_anotacoes():
        tree.delete(*tree.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.nome, a.data, a.conteudo
            FROM anotacoes a
            JOIN paciente p ON a.paciente_id = p.id
            ORDER BY a.data DESC
        """)
        for anotacao in cur.fetchall():
            id_, paciente, data_iso, conteudo = anotacao
            try:
                data_br = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                data_br = data_iso
            tree.insert('', tk.END, values=(id_, paciente, data_br, conteudo))
        conn.close()

    def limpar_campos():
        paciente_combobox.set("")
        data_entry.delete(0, tk.END)
        conteudo_text.delete("1.0", tk.END)

    def adicionar_anotacao():
        paciente_valor = paciente_combobox.get()
        data = data_entry.get()
        conteudo = conteudo_text.get("1.0", tk.END).strip()

        if not paciente_valor or not data or not conteudo:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            paciente_id = int(paciente_valor.split(" - ")[0])
            data_iso = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO anotacoes (paciente_id, data, conteudo) VALUES (?, ?, ?)", (paciente_id, data_iso, conteudo))
        conn.commit()
        conn.close()
        carregar_anotacoes()
        limpar_campos()

    def selecionar_anotacao(event):
        selecionado = tree.focus()
        if selecionado:
            valores = tree.item(selecionado)['values']
            anotacao_id = valores[0]
            paciente_nome = valores[1]
            data_br = valores[2]
            conteudo = valores[3]

            paciente_combobox.set(next((v for v in paciente_combobox["values"] if paciente_nome in v), ""))
            data_entry.delete(0, tk.END)
            data_entry.insert(0, data_br)
            conteudo_text.delete("1.0", tk.END)
            conteudo_text.insert(tk.END, conteudo)

    def editar_anotacao():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma anotação para editar.")
            return

        anotacao_id = tree.item(selecionado)['values'][0]
        paciente_valor = paciente_combobox.get()
        data = data_entry.get()
        conteudo = conteudo_text.get("1.0", tk.END).strip()

        if not paciente_valor or not data or not conteudo:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            paciente_id = int(paciente_valor.split(" - ")[0])
            data_iso = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE anotacoes SET paciente_id = ?, data = ?, conteudo = ? WHERE id = ?", (paciente_id, data_iso, conteudo, anotacao_id))
        conn.commit()
        conn.close()
        carregar_anotacoes()
        limpar_campos()

    def excluir_anotacao():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma anotação para excluir.")
            return
        anotacao_id = tree.item(selecionado)['values'][0]
        if messagebox.askyesno("Confirmação", "Deseja excluir esta anotação?"):
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM anotacoes WHERE id = ?", (anotacao_id,))
            conn.commit()
            conn.close()
            carregar_anotacoes()
            limpar_campos()

    tree.bind("<<TreeviewSelect>>", selecionar_anotacao)

    btn_frame = ttk.Frame(frame_principal)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Adicionar", command=adicionar_anotacao).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Editar", command=editar_anotacao).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Excluir", command=excluir_anotacao).grid(row=0, column=2, padx=5)

    carregar_anotacoes()
