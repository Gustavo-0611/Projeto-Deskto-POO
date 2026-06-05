import os
import banco


def setup():
    if os.path.exists("loja_test.db"):
        os.remove("loja_test.db")
    banco.DB = "loja_test.db"
    banco.criar_tabelas()


def test_salvar_produto():
    banco.salvar_produto("Roupa", "Camiseta", 49.90, "M")
    rows = banco.listar_produtos()
    assert len(rows) == 1
    assert rows[0][1] == "Camiseta"
    print("  [OK] salvar produto")


def test_remover_produto():
    banco.remover_produto("Camiseta")
    rows = banco.listar_produtos()
    assert len(rows) == 0
    print("  [OK] remover produto")


def test_registrar_compra():
    banco.registrar_compra("Ana", 149.80)
    rows = banco.listar_compras()
    assert len(rows) == 1
    assert rows[0][1] == "Ana"
    assert rows[0][2] == 149.80
    print("  [OK] registrar compra")


def teardown():
    if os.path.exists("loja_test.db"):
        os.remove("loja_test.db")
    banco.DB = "loja.db"


if __name__ == "__main__":
    print("\n--- Testbench: Banco de Dados ---")
    setup()
    test_salvar_produto()
    test_remover_produto()
    test_registrar_compra()
    teardown()
    print()
