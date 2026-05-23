from package.produtos import Roupa, Eletronico, Alimento
from package.carrinho_pkg import Carrinho
from package.caixa_pkg import Caixa


def test_adicionar():
    c = Carrinho()
    c.adicionar(Roupa("Camiseta", 49.90, "M"))
    c.adicionar(Eletronico("Fone", 199.90, 12))
    assert len(c.produtos) == 2
    print("  [OK] adicionar")


def test_remover():
    c = Carrinho()
    c.adicionar(Alimento("Chocolate", 8.50, "12/2025"))
    c.remover("Chocolate")
    assert len(c.produtos) == 0
    print("  [OK] remover")


def test_remover_inexistente():
    c = Carrinho()
    c.remover("Inexistente")
    print("  [OK] remover inexistente")


def test_total():
    c = Carrinho()
    c.adicionar(Roupa("Calça", 119.90, "42"))
    c.adicionar(Alimento("Café", 22.00, "06/2026"))
    assert c.total() == 141.90
    print("  [OK] total")


def test_carrinho_vazio():
    c = Carrinho()
    caixa = Caixa("Ana")
    caixa.finalizar_compra(c)
    print("  [OK] carrinho vazio")


def test_finalizar_compra():
    c = Carrinho()
    c.adicionar(Roupa("Camiseta", 49.90, "M"))
    c.adicionar(Eletronico("Carregador", 59.90, 6))
    caixa = Caixa("Carlos")
    caixa.finalizar_compra(c)
    print("  [OK] finalizar compra")


if __name__ == "__main__":
    print("\n--- Testbench: Carrinho e Caixa ---")
    test_adicionar()
    test_remover()
    test_remover_inexistente()
    test_total()
    test_carrinho_vazio()
    test_finalizar_compra()
    print()
