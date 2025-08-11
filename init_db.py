import os
import sqlite3

def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn = sqlite3.connect('database/site.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trabalhos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descricao TEXT,
            imagem_antes TEXT,
            imagem_depois TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            url TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco criado e tabelas inicializadas com sucesso!")

if __name__ == '__main__':
    init_db()
