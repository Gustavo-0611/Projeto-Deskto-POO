import sqlite3


DB = "loja.db"


def conectar():
    return sqlite3.connect(DB)


def criar_tabelas():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            nome TEXT,
            preco REAL,
            extra TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operador TEXT,
            total REAL,
            data TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
    con.commit()
    con.close()


def salvar_produto(tipo: str, nome: str, preco: float, extra: str):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO produtos (tipo, nome, preco, extra) VALUES (?, ?, ?, ?)",
        (tipo, nome, preco, extra)
    )
    con.commit()
    con.close()


def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT tipo, nome, preco, extra FROM produtos")
    rows = cur.fetchall()
    con.close()
    return rows


def remover_produto(nome: str):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM produtos WHERE nome = ?", (nome,))
    con.commit()
    con.close()


def registrar_compra(operador: str, total: float):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO compras (operador, total) VALUES (?, ?)",
        (operador, total)
    )
    con.commit()
    con.close()


def listar_compras():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, operador, total, data FROM compras")
    rows = cur.fetchall()
    con.close()
    return rows
