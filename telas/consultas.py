import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from criar_tabelas import conectar

def janela_consultas():
    janela = tk.Toplevel()
    janela.title("Gerenciar Consultas")
    janela.geometry("800x500")
    janela.configure(bg="#f7f6f2")

    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10))

    frame = ttk.Frame(janela)
    frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

    tree = ttk.Treeview(frame, columns=("ID", "Paciente", "Data", "Hora"), show="headings", height=10)
    for col in ("ID", "Paciente", "Data", "Hora"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)
    tree.pack(expand=True, fill=tk.BOTH, pady=10)

    def carregar_consultas():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT consultas.id, pacientes.nome, consultas.data, consultas.horario
            FROM consultas
            JOIN pacientes ON consultas.paciente_id = pacientes.id
            ORDER BY consultas.data
        """)
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)
        conn.close()

    carregar_consultas()

    # Inputs
    input_frame = ttk.Frame(janela)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Paciente ID:").grid(row=0, column=0, padx=5, pady=5)
    entry_paciente_id = ttk.Entry(input_frame, width=10)
    entry_paciente_id.grid(row=0, column=1, padx=5)

    ttk.Label(input_frame, text="Data (DDMMYYYY):").grid(row=0, column=2, padx=5)
    entry_data = ttk.Entry(input_frame, width=15)
    entry_data.grid(row=0, column=3, padx=5)

    ttk.Label(input_frame, text="Horário (HHMM):").grid(row=0, column=4, padx=5)
    entry_horario = ttk.Entry(input_frame, width=10)
    entry_horario.grid(row=0, column=5, padx=5)

    def adicionar_consulta():
        paciente_id = entry_paciente_id.get()
        data = entry_data.get()
        horario = entry_horario.get()

        if not paciente_id.strip() or not data.strip() or not horario.strip():
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO consultas (paciente_id, data, horario) VALUES (?, ?, ?)", (paciente_id, data, horario))
            conn.commit()
            messagebox.showinfo("Sucesso", "Consulta adicionada.")
            carregar_consultas()
            entry_paciente_id.delete(0, tk.END)
            entry_data.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar consulta: {e}")
        finally:
            conn.close()

    def editar_consulta():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta para editar.")
            return

        consulta_id = tree.item(selected)['values'][0]
        novo_paciente_id = entry_paciente_id.get()
        nova_data = entry_data.get()
        novo_horario = entry_horario.get()

        if not novo_paciente_id.strip() or not nova_data.strip() or not novo_horario.strip():
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE consultas
                SET paciente_id = ?, data = ?, horario = ?
                WHERE id = ?
            """, (novo_paciente_id, nova_data, novo_horario, consulta_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Consulta atualizada.")
            carregar_consultas()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao editar: {e}")
        finally:
            conn.close()

    def excluir_consulta():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma consulta para excluir.")
            return
        consulta_id = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirmação", "Deseja excluir esta consulta?")
        if confirm:
            conn = conectar()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Consulta excluída.")
                carregar_consultas()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")
            finally:
                conn.close()

    # Botões
    botoes = ttk.Frame(janela)
    botoes.pack(pady=10)

    estilo_botao = {"style": "TButton"}
    ttk.Button(botoes, text="➕ Adicionar", command=adicionar_consulta, **estilo_botao).grid(row=0, column=0, padx=5)
    ttk.Button(botoes, text="✏️ Editar", command=editar_consulta, **estilo_botao).grid(row=0, column=1, padx=5)
    ttk.Button(botoes, text="❌ Excluir", command=excluir_consulta, **estilo_botao).grid(row=0, column=2, padx=5)
