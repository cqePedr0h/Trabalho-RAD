import tkinter as tk
from tkinter import ttk, messagebox
from criar_tabelas import conectar

def janela_anotacoes():
    janela = tk.Toplevel()
    janela.title("Gerenciar Anotações")
    janela.geometry("650x450")

    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    frame = ttk.Frame(janela, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Consulta", "Conteúdo"), show="headings")
    tree.heading("ID", text="ID")
    tree.column("ID", width=50, anchor="center")
    tree.heading("Consulta", text="Consulta")
    tree.column("Consulta", width=200, anchor="center")
    tree.heading("Conteúdo", text="Conteúdo")
    tree.column("Conteúdo", anchor="w")
    tree.pack(fill=tk.BOTH, expand=True)

    def carregar_anotacoes():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT anotacoes.id, pacientes.nome || ' - ' || consultas.data || ' ' || consultas.horario AS consulta_info,
                   anotacoes.conteudo
            FROM anotacoes
            JOIN consultas ON anotacoes.consulta_id = consultas.id
            JOIN pacientes ON consultas.paciente_id = pacientes.id
            ORDER BY anotacoes.id DESC
        """)
        anotacoes = cur.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for a in anotacoes:
            tree.insert("", "end", values=a)

    def adicionar_anotacao():
        def salvar():
            selected = combo_consultas.get()
            conteudo = text_conteudo.get("1.0", tk.END).strip()

            if not selected or not conteudo:
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            consulta_id = consulta_ids.get(selected)
            if not consulta_id:
                messagebox.showerror("Erro", "Consulta inválida.")
                return

            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO anotacoes (consulta_id, conteudo) VALUES (?, ?)", (consulta_id, conteudo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Anotação adicionada.")
            janela_add.destroy()
            carregar_anotacoes()

        janela_add = tk.Toplevel(janela)
        janela_add.title("Adicionar Anotação")
        janela_add.geometry("400x300")
        janela_add.grab_set()

        ttk.Label(janela_add, text="Consulta:").pack(pady=5)

        combo_consultas = ttk.Combobox(janela_add, state="readonly")
        combo_consultas.pack(fill=tk.X, padx=10)

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT consultas.id, pacientes.nome || ' - ' || consultas.data || ' ' || consultas.horario
            FROM consultas
            JOIN pacientes ON consultas.paciente_id = pacientes.id
        """)
        dados = cur.fetchall()
        conn.close()

        consulta_ids = {label: cid for cid, label in dados}
        combo_consultas["values"] = list(consulta_ids.keys())

        ttk.Label(janela_add, text="Conteúdo:").pack(pady=5)
        text_conteudo = tk.Text(janela_add, height=10)
        text_conteudo.pack(fill=tk.BOTH, padx=10, pady=5)

        ttk.Button(janela_add, text="Salvar", command=salvar).pack(pady=10)

    def excluir_anotacao():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma anotação para excluir.")
            return
        id_anotacao = tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirmação", "Deseja excluir esta anotação?")
        if confirm:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM anotacoes WHERE id=?", (id_anotacao,))
            conn.commit()
            conn.close()
            carregar_anotacoes()

    frame_botoes = ttk.Frame(janela)
    frame_botoes.pack(pady=10)

    ttk.Button(frame_botoes, text="Adicionar Anotação", command=adicionar_anotacao).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botoes, text="Excluir Anotação", command=excluir_anotacao).grid(row=0, column=1, padx=5)

    carregar_anotacoes()
