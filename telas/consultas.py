import tkinter as tk
from tkinter import ttk, messagebox
from criar_tabelas import conectar
import re

def janela_consultas():
    janela = tk.Toplevel()
    janela.title("Agendar Consultas")
    janela.geometry("750x500")
    janela.configure(bg="#f7f6f2")
    janela.iconbitmap("logos/favicon.ico")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Paciente:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame, text="Data (DD/MM/AAAA):", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame, text="Hora (HH:MM):", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=6)
    ttk.Label(frame, text="Descrição:", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="nw", padx=5, pady=6)

    pacientes = []
    pacientes_ids = {}

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM paciente")
    for pid, nome in cur.fetchall():
        pacientes.append(nome)
        pacientes_ids[nome] = pid
    conn.close()

    paciente_cb = ttk.Combobox(frame, values=pacientes, font=("Segoe UI", 12), width=47, state="readonly")
    paciente_cb.grid(row=0, column=1, pady=6)

    def mascara_data(event):
        texto = data_entry.get().replace("/", "")[:8]
        novo = ""
        for i in range(len(texto)):
            if i in [2, 4]:
                novo += "/"
            novo += texto[i]
        data_entry.delete(0, tk.END)
        data_entry.insert(0, novo)

    def mascara_hora(event):
        texto = hora_entry.get().replace(":", "")[:4]
        novo = ""
        for i in range(len(texto)):
            if i == 2:
                novo += ":"
            novo += texto[i]
        hora_entry.delete(0, tk.END)
        hora_entry.insert(0, novo)

    data_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=50)
    data_entry.grid(row=1, column=1, pady=6)
    data_entry.bind("<KeyRelease>", mascara_data)

    hora_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=50)
    hora_entry.grid(row=2, column=1, pady=6)
    hora_entry.bind("<KeyRelease>", mascara_hora)

    descricao_text = tk.Text(frame, font=("Segoe UI", 12), height=4, width=50)
    descricao_text.grid(row=3, column=1, pady=6)

    tree = ttk.Treeview(frame, columns=("ID", "Paciente", "Data", "Hora", "Descrição"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

    frame.grid_rowconfigure(5, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    def carregar_consultas():
        tree.delete(*tree.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT consultas.id, paciente.nome, consultas.data, consultas.hora, consultas.descricao
            FROM consultas
            JOIN paciente ON consultas.paciente_id = paciente.id
            ORDER BY consultas.data, consultas.hora
        """)
        for linha in cur.fetchall():
            tree.insert("", tk.END, values=linha)
        conn.close()

    def validar_data(data):
        return re.match(r"^\d{2}/\d{2}/\d{4}$", data)

    def validar_hora(hora):
        return re.match(r"^\d{2}:\d{2}$", hora)

    def agendar_consulta():
        paciente = paciente_cb.get()
        data = data_entry.get().strip()
        hora = hora_entry.get().strip()
        descricao = descricao_text.get("1.0", tk.END).strip()

        if not paciente or not data or not hora:
            messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        if not validar_data(data):
            messagebox.showwarning("Formato inválido", "A data deve estar no formato DD/MM/AAAA.")
            return

        if not validar_hora(hora):
            messagebox.showwarning("Formato inválido", "A hora deve estar no formato HH:MM.")
            return

        paciente_id = pacientes_ids.get(paciente)

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO consultas (paciente_id, data, hora, descricao) VALUES (?, ?, ?, ?)",
                    (paciente_id, data, hora, descricao))
        conn.commit()
        conn.close()
        carregar_consultas()
        limpar_campos()

    def limpar_campos():
        paciente_cb.set("")
        data_entry.delete(0, tk.END)
        hora_entry.delete(0, tk.END)
        descricao_text.delete("1.0", tk.END)

    def excluir_consulta():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma consulta para excluir.")
            return
        consulta_id = tree.item(selecionado)["values"][0]
        if messagebox.askyesno("Confirmação", "Deseja excluir esta consulta?"):
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM consultas WHERE id=?", (consulta_id,))
            conn.commit()
            conn.close()
            carregar_consultas()

    frame_botoes = ttk.Frame(frame)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(frame_botoes, text="Agendar", command=agendar_consulta).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botoes, text="Excluir", command=excluir_consulta).grid(row=0, column=1, padx=5)

    carregar_consultas()
