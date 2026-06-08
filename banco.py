import sqlite3
import json


DB = "loja.db"


def conectar():
    return sqlite3.connect(DB)


def criar_tabelas():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS carrinho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            objeto TEXT
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


def serializar(produto) -> str:
    dados = {
        "tipo": type(produto).__name__,
        "nome": produto.nome,
        "preco": produto.preco
    }
    if hasattr(produto, "tamanho"):
        dados["tamanho"] = produto.tamanho
    elif hasattr(produto, "garantia"):
        dados["garantia"] = produto.garantia
    elif hasattr(produto, "validade"):
        dados["validade"] = produto.validade
    return json.dumps(dados)


def desserializar(texto: str):
    from package.produtos import Roupa, Eletronico, Alimento
    dados = json.loads(texto)
    tipo = dados["tipo"]
    if tipo == "Roupa":
        return Roupa(dados["nome"], dados["preco"], dados["tamanho"])
    elif tipo == "Eletronico":
        return Eletronico(dados["nome"], dados["preco"], dados["garantia"])
    elif tipo == "Alimento":
        return Alimento(dados["nome"], dados["preco"], dados["validade"])


def salvar_objeto(produto):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO carrinho (nome, objeto) VALUES (?, ?)",
        (produto.nome, serializar(produto))
    )
    con.commit()
    con.close()


def carregar_objetos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT objeto FROM carrinho")
    rows = cur.fetchall()
    con.close()
    return [desserializar(row[0]) for row in rows]


def remover_objeto(nome: str):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM carrinho WHERE nome = ?", (nome,))
    con.commit()
    con.close()


def limpar_carrinho():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM carrinho")
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