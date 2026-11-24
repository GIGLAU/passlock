import sqlite3

DB_NAME = "data/passlock.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credenciais(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servico TEXT NOT NULL,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL,
        observacao TEXT
    )
    """)

    conn.commit()
    conn.close()


def adicionar(servico, usuario, senha, observacao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO credenciais
    (servico, usuario, senha, observacao)
    VALUES (?, ?, ?, ?)
    """, (servico, usuario, senha, observacao))

    conn.commit()
    conn.close()


def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM credenciais")

    dados = cursor.fetchall()

    conn.close()

    return dados


def excluir(id_registro):
    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM credenciais WHERE id = ?",
        (id_registro,)
    )

    conn.commit()
    conn.close()
