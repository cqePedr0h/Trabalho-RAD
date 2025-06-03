import tkinter as tk
from tkinter import ttk
from telas import pacientes, consultas, anotacoes

def main():
    root = tk.Tk()
    root.title("Sistema de Terapia Holística")
    root.geometry("900x600")
    root.configure(bg="#f7f6f2")

    # Estilo para ttk.Botões
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 12), padding=10)
    
    # Frame central
    frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    titulo = tk.Label(frame, text="Sistema de Gestão do Terapeuta Holístico", 
                      font=("Segoe UI", 20, "bold"), bg="#ffffff", fg="#3e3e3e")
    titulo.pack(pady=(20, 10), padx=20)

    subtitulo = tk.Label(frame, text="Selecione uma opção abaixo:", 
                         font=("Segoe UI", 12), bg="#ffffff", fg="#666666")
    subtitulo.pack(pady=(0, 20))

    # Botões
    btn_pacientes = ttk.Button(frame, text="📋 Gerenciar Pacientes", command=pacientes.janela_pacientes)
    btn_pacientes.pack(pady=10)

    btn_consultas = ttk.Button(frame, text="📅 Gerenciar Consultas", command=consultas.janela_consultas)
    btn_consultas.pack(pady=10)

    btn_anotacoes = ttk.Button(frame, text="📝 Gerenciar Anotações", command=anotacoes.janela_anotacoes)
    btn_anotacoes.pack(pady=10)

    # Rodapé
    rodape = tk.Label(root, text="© 2025 Terapia Holística - Projeto Acadêmico", 
                      font=("Segoe UI", 9), bg="#f7f6f2", fg="#888888")
    rodape.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
