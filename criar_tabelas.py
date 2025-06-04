import sqlite3

conn = sqlite3.connect("paciente.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS paciente (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Telefone INTEGER NOT NULL,
    Email TEXT NOT NULL                         
)
""")

conn.commit()
conn.close()

def conectar():
    return sqlite3.connect("paciente.db")
