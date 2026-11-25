import sqlite3
import hashlib

DB_NAME = "data/passlock.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credenciais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servico TEXT NOT NULL,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL,
        observacao TEXT
    )
    """)

    conn.commit()
    conn.close()


def criar_tabela_master():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracao (
        id INTEGER PRIMARY KEY,
        master_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def salvar_master(password):
    conn = conectar()
    cursor = conn.cursor()

    hash_senha = hashlib.sha256(
        password.encode()
    ).hexdigest()

    cursor.execute(
        "INSERT INTO configuracao (id, master_hash) VALUES (1, ?)",
        (hash_senha,)
    )

    conn.commit()
    conn.close()


def validar_master(password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT master_hash FROM configuracao WHERE id = 1"
    )

    resultado = cursor.fetchone()

    conn.close()

    if not resultado:
        return False

    hash_digitado = hashlib.sha256(
        password.encode()
    ).hexdigest()

    return hash_digitado == resultado[0]


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

    cursor.execute(
        "SELECT * FROM credenciais"
    )

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