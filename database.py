import sqlite3

def conectar():
    return sqlite3.connect("terapeuta.db")

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    # Tabela de Pacientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nasc TEXT,
            telefone TEXT,
            email TEXT
        )
    """)

    # Tabela de Consultas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data TEXT,
            horario TEXT,
            descricao TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    # Tabela de Anotações
    cur.execute("""
        CREATE TABLE IF NOT EXISTS anotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulta_id INTEGER,
            conteudo TEXT,
            FOREIGN KEY (consulta_id) REFERENCES consultas(id)
        )
    """)

    con.commit()
    con.close()
