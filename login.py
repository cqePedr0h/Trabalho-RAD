import tkinter as tk
from tkinter import ttk, messagebox
from main import main  # Importa sua janela principal

def login():
    def verificar_login():
        usuario = entry_usuario.get().strip()
        if not usuario:
            messagebox.showwarning("Aviso", "Digite um nome de usuário.")
            return
        login_janela.destroy()
        main()

    login_janela = tk.Tk()
    login_janela.title("Login - Sistema de Terapia Holística")
    login_janela.geometry("400x250")
    login_janela.configure(bg="#f7f6f2")

    frame = tk.Frame(login_janela, bg="#ffffff", bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Bem-vindo(a)", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=10)
    tk.Label(frame, text="Digite seu nome de usuário:", font=("Segoe UI", 11), bg="#ffffff").pack(pady=(5, 0))

    entry_usuario = ttk.Entry(frame, font=("Segoe UI", 11))
    entry_usuario.pack(pady=10, padx=20)

    ttk.Button(frame, text="Entrar", command=verificar_login).pack(pady=10)

    login_janela.mainloop()
