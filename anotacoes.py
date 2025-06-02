import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import conectar

def janela_anotacoes():
    janela = tk.Toplevel()
    janela.title("Anotações do Terapeuta Holístico")
    janela.geometry("800x600")
    janela.configure(bg="#f7f6f2")  # Cor suave de fundo

    # Título estilizado
    tk.Label(
        janela,
        text="Anotações do Terapeuta Holístico",
        font=("Segoe UI", 18, "bold"),
        bg="#f7f6f2",
        fg="#3e3e3e"
    ).pack(pady=10)

    # Criação das abas
    tab_control = ttk.Notebook(janela)
    tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tab_consultas = ttk.Frame(tab_control)
    tab_anotacoes = ttk.Frame(tab_control)

    tab_control.add(tab_consultas, text='Consultas')
    tab_control.add(tab_anotacoes, text='Anotações')

    # --- CONSULTAS TAB ---
    tree_consultas = ttk.Treeview(tab_consultas, columns=("ID", "Paciente", "Data", "Hora"), show='headings')
    for col in ("ID", "Paciente", "Data", "Hora"):
        tree_consultas.heading(col, text=col)
        tree_consultas.column(col, width=100, anchor="center")
    tree_consultas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def carregar_consultas():
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT consultas.id, pacientes.nome, consultas.data, consultas.horario
            FROM consultas
            JOIN pacientes ON consultas.paciente_id = pacientes.id
            ORDER BY consultas.data
        """)
        consultas = cur.fetchall()
        con.close()

        for row in tree_consultas.get_children():
            tree_consultas.delete(row)
        for c in consultas:
            tree_consultas.insert('', 'end', values=c)

    carregar_consultas()

    # --- ANOTAÇÕES TAB ---
    frame_anotacoes = tk.Frame(tab_anotacoes, bg="#f7f6f2")
    frame_anotacoes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    label_anotacoes = tk.Label(
        frame_anotacoes,
        text="Anotações da Consulta Selecionada:",
        font=("Segoe UI", 12, "bold"),
        bg="#f7f6f2"
    )
    label_anotacoes.pack(anchor='w', padx=10, pady=(0,5))

    text_anotacoes = tk.Text(frame_anotacoes, height=6, font=("Segoe UI", 10))
    text_anotacoes.pack(fill=tk.BOTH, expand=True, padx=10)

    label_nova = tk.Label(
        frame_anotacoes,
        text="Nova anotação:",
        font=("Segoe UI", 11),
        bg="#f7f6f2"
    )
    label_nova.pack(anchor='w', padx=10, pady=(10,0))

    entry_nova_anotacao = tk.Entry(frame_anotacoes, width=100, font=("Segoe UI", 10))
    entry_nova_anotacao.pack(padx=10, pady=(0,5))

    def exibir_anotacoes(event):
        selected = tree_consultas.focus()
        if not selected:
            return
        consulta_id = tree_consultas.item(selected)['values'][0]

        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT conteudo FROM anotacoes WHERE consulta_id = ?", (consulta_id,))
        anotacoes = cur.fetchall()
        con.close()

        text_anotacoes.delete("1.0", tk.END)
        for a in anotacoes:
            text_anotacoes.insert(tk.END, f"- {a[0]}\n")

    tree_consultas.bind("<<TreeviewSelect>>", exibir_anotacoes)

    def adicionar_anotacao():
        selected = tree_consultas.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta.")
            return

        consulta_id = tree_consultas.item(selected)['values'][0]
        conteudo = entry_nova_anotacao.get()

        if not conteudo:
            messagebox.showwarning("Aviso", "Digite uma anotação.")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO anotacoes (consulta_id, conteudo) VALUES (?, ?)", (consulta_id, conteudo))
        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Anotação adicionada.")
        entry_nova_anotacao.delete(0, tk.END)
        exibir_anotacoes(None)

    btn_add = tk.Button(
        frame_anotacoes,
        text="Adicionar Anotação",
        command=adicionar_anotacao,
        bg="#7ca6a1",
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    btn_add.pack(pady=5)
