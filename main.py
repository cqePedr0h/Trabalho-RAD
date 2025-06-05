import tkinter as tk
from tkinter import ttk
from telas import pacientes, consultas, anotacoes
from login import janela_login
from criar_tabelas import criar_tabelas

def abrir_tela_principal():
    janela_principal = tk.Tk()
    janela_principal.title("Sistema Terapeuta Holístico")
    largura = 700
    altura = 450

    
    x = (janela_principal.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela_principal.winfo_screenheight() // 2) - (altura // 2)
    janela_principal.geometry(f"{largura}x{altura}+{x}+{y}")
    janela_principal.configure(bg="#f7f6f2")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10)
    estilo.configure("TLabel", font=("Segoe UI", 14))

    frame = ttk.Frame(janela_principal, padding=30)
    frame.place(relx=0.5, rely=0.5, anchor="center")  

    ttk.Label(
        frame,
        text="Bem-vindo ao Sistema do Terapeuta Holístico",
        font=("Segoe UI", 16, "bold"),
        anchor="center"
    ).pack(pady=(0, 30))

    ttk.Button(frame, text="Pacientes", width=25, command=pacientes.janela_pacientes).pack(pady=10)
    ttk.Button(frame, text="Consultas", width=25, command=consultas.janela_consultas).pack(pady=10)
    ttk.Button(frame, text="Anotações", width=25, command=anotacoes.janela_anotacoes).pack(pady=10)

    janela_principal.mainloop()

if __name__ == "__main__":
    criar_tabelas()
    root = tk.Tk()
    root.withdraw()  
    janela_login(root, abrir_tela_principal)
    root.mainloop()
