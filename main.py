import tkinter as tk
from tkinter import ttk
from telas import pacientes, consultas
import telas.anotacoes as anotacoes

def main():
    #janela principal
    janela = tk.Tk()
    janela.title("Sistema do Terapeuta Holístico")
    janela.geometry("400x300")
    janela.configure(bg="#f5f5f5")  # Cor de fundo 

    # Aplicar estilo aos widgets
    style = ttk.Style()
    style.theme_use('clam')  
    style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="#003c32", padding=6)
    style.configure("TLabel", font=("Helvetica", 10))
    style.configure("TFrame", background="#f5f5f5")

    # Frame principal para centralizar os botões
    frame = ttk.Frame(janela, padding=20)
    frame.pack(expand=True)

    # Título
    ttk.Label(frame, text="Bem-vindo ao Sistema do Terapeuta").pack(pady=(0, 20))

    # Botões principais
    ttk.Button(frame, text="Gerenciar Pacientes", width=25, command=pacientes.janela_pacientes).pack(pady=5)
    ttk.Button(frame, text="Gerenciar Consultas", width=25, command=consultas.janela_consultas).pack(pady=5)
    ttk.Button(frame, text="Anotações do Terapeuta", width=25, command=anotacoes.janela_anotacoes).pack(pady=5)

    # Iniciar a aplicação
    janela.mainloop()

if __name__ == "__main__":
    main()
