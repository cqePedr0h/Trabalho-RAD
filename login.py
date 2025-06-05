import tkinter as tk
from tkinter import ttk, messagebox
from criar_tabelas import conectar
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def janela_login(root, abrir_janela_principal):
    janela = tk.Toplevel(root)
    janela.title("Login")
    janela.geometry("400x250")
    janela.configure(bg="#f7f6f2")

    janela.update_idletasks()
    largura = 400
    altura = 250
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

    frame = ttk.Frame(janela, padding=20)
    frame.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame, text="Usuário:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=5)
    usuario_entry = ttk.Entry(frame, font=("Segoe UI", 11))
    usuario_entry.grid(row=0, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Senha:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=5)
    senha_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 11))
    senha_entry.grid(row=1, column=1, pady=5, sticky="ew")

    frame.grid_columnconfigure(1, weight=1)

    def validar_login():
        usuario = usuario_entry.get().strip()
        senha = senha_entry.get()
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha usuário e senha.")
            return
        senha_h = hash_senha(senha)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_h))
        if cur.fetchone():
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario}!")
            janela.destroy()
            abrir_janela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        conn.close()

    def cadastrar_usuario():
        usuario = usuario_entry.get().strip()
        senha = senha_entry.get()
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha usuário e senha para cadastro.")
            return
        senha_h = hash_senha(senha)
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_h))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cadastro: {e}")
        finally:
            conn.close()

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    ttk.Button(btn_frame, text="Login", command=validar_login).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Cadastrar", command=cadastrar_usuario).grid(row=0, column=1, padx=10)

    return janela
