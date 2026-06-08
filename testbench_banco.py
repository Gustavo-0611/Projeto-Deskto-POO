import os
import banco
from package.produtos import Roupa, Eletronico, Alimento


def setup():
    banco.DB = "loja_test.db"
    if os.path.exists(banco.DB):
        os.remove(banco.DB)
    banco.criar_tabelas()


def test_serializar_roupa():
    p = Roupa("Camiseta", 49.90, "M")
    banco.salvar_objeto(p)
    objetos = banco.carregar_objetos()
    assert isinstance(objetos[0], Roupa)
    assert objetos[0].nome == "Camiseta"
    assert objetos[0].tamanho == "M"
    print("  [OK] serializar Roupa")


def test_serializar_eletronico():
    p = Eletronico("Fone", 199.90, 12)
    banco.salvar_objeto(p)
    objetos = banco.carregar_objetos()
    assert isinstance(objetos[1], Eletronico)
    assert objetos[1].garantia == 12
    print("  [OK] serializar Eletronico")


def test_serializar_alimento():
    p = Alimento("Cafe", 22.00, "06/2026")
    banco.salvar_objeto(p)
    objetos = banco.carregar_objetos()
    assert isinstance(objetos[2], Alimento)
    assert objetos[2].validade == "06/2026"
    print("  [OK] serializar Alimento")


def test_remover_objeto():
    banco.remover_objeto("Camiseta")
    objetos = banco.carregar_objetos()
    assert all(o.nome != "Camiseta" for o in objetos)
    print("  [OK] remover objeto")


def test_limpar_carrinho():
    banco.limpar_carrinho()
    assert len(banco.carregar_objetos()) == 0
    print("  [OK] limpar carrinho")


def test_registrar_compra():
    banco.registrar_compra("Ana", 149.80)
    rows = banco.listar_compras()
    assert rows[0][1] == "Ana"
    assert rows[0][2] == 149.80
    print("  [OK] registrar compra")


def teardown():
    if os.path.exists(banco.DB):
        os.remove(banco.DB)
    banco.DB = "loja.db"


if __name__ == "__main__":
    print("\n--- Testbench: Banco de Dados ---")
    setup()
    test_serializar_roupa()
    test_serializar_eletronico()
    test_serializar_alimento()
    test_remover_objeto()
    test_limpar_carrinho()
    test_registrar_compra()
    teardown()
    print()