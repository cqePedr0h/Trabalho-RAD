import sqlite3

def conectar():
    # Conecta ao arquivo do banco SQLite (cria se não existir)
    return sqlite3.connect('banco_terapeuta.db')
