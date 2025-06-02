import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import conectar

def janela_consultas():
    janela = tk.Toplevel()
    janela.title("Gerenciar Consultas")
    janela.geometry("750x450")
    janela.configure(bg="#f5f5f5")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="#004d40", padding=6)
    style.configure("TLabel", font=("Helvetica", 10), background="#f5f5f5")
    style.configure("TEntry", padding=5)
    style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    def carregar_consultas():
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT consultas.id, pacientes.nome, consultas.data, consultas.horario
            FROM consultas
            JOIN pacientes ON consultas.paciente_id = pacientes.id
            ORDER BY consultas.data
        """)
        dados = cur.fetchall()
        con.close()

        for row in tree.get_children():
            tree.delete(row)
        for consulta in dados:
            tree.insert('', 'end', values=consulta)

    def carregar_pacientes():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, nome FROM pacientes ORDER BY nome")
        pacientes_lista = cur.fetchall()
        con.close()
        combo_paciente['values'] = [f"{p[0]} - {p[1]}" for p in pacientes_lista]

    def adicionar_consulta():
        paciente_info = combo_paciente.get()
        if not paciente_info or "-" not in paciente_info:
            messagebox.showwarning("Aviso", "Selecione um paciente.")
            return

        paciente_id = paciente_info.split(" - ")[0]
        data = entry_data.get()
        horario = entry_horario.get()

        if not data or not horario:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO consultas (paciente_id, data, horario) VALUES (?, ?, ?)",
                    (paciente_id, data, horario))
        con.commit()
        con.close()

        carregar_consultas()
        entry_data.delete(0, tk.END)
        entry_horario.delete(0, tk.END)

    def excluir_consulta():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta para excluir.")
            return

        consulta_id = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir esta consulta?")
        if confirm:
            con = conectar()
            cur = con.cursor()
            cur.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
            con.commit()
            con.close()
            carregar_consultas()

    def editar_consulta():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta para editar.")
            return

        consulta_id = tree.item(selected)['values'][0]
        paciente_info = combo_paciente.get()
        if not paciente_info or "-" not in paciente_info:
            messagebox.showwarning("Aviso", "Selecione um paciente.")
            return

        paciente_id = paciente_info.split(" - ")[0]
        data = entry_data.get()
        horario = entry_horario.get()

        if not data or not horario:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE consultas SET paciente_id = ?, data = ?, horario = ? WHERE id = ?",
                    (paciente_id, data, horario, consulta_id))
        con.commit()
        con.close()
        carregar_consultas()

    def preencher_campos(event):
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected)['values']
        consulta_id, paciente_nome, data, horario = values
        entry_data.delete(0, tk.END)
        entry_data.insert(0, data)
        entry_horario.delete(0, tk.END)
        entry_horario.insert(0, horario)
        # Tenta encontrar o paciente correspondente na combo
        for item in combo_paciente['values']:
            if paciente_nome in item:
                combo_paciente.set(item)
                break

    # Frame de formulário
    frame = ttk.Frame(janela, padding=10)
    frame.pack(fill=tk.X)

    ttk.Label(frame, text="Paciente:").grid(row=0, column=0, sticky=tk.W, pady=2)
    combo_paciente = ttk.Combobox(frame, width=30)
    combo_paciente.grid(row=0, column=1, pady=2, padx=5)

    ttk.Label(frame, text="Data (AAAA-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_data = ttk.Entry(frame, width=30)
    entry_data.grid(row=1, column=1, pady=2, padx=5)

    ttk.Label(frame, text="Horário (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_horario = ttk.Entry(frame, width=30)
    entry_horario.grid(row=2, column=1, pady=2, padx=5)

    ttk.Button(frame, text="Adicionar", command=adicionar_consulta).grid(row=3, column=0, pady=10)
    ttk.Button(frame, text="Editar", command=editar_consulta).grid(row=3, column=1, pady=10, sticky=tk.W)
    ttk.Button(frame, text="Excluir", command=excluir_consulta).grid(row=3, column=1, pady=10, sticky=tk.E)

    # Tabela de consultas
    tree = ttk.Treeview(janela, columns=("ID", "Paciente", "Data", "Horário"), show="headings")
    for col in ("ID", "Paciente", "Data", "Horário"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tree.bind("<<TreeviewSelect>>", preencher_campos)

    carregar_pacientes()
    carregar_consultas()
