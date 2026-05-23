from package.produtos import Roupa, Eletronico, Alimento


def test_roupa():
    r = Roupa("Camiseta", 49.90, "M")
    assert r.nome == "Camiseta"
    assert r.preco == 49.90
    assert r.tamanho == "M"
    assert "Tamanho: M" in r.descricao()
    print("  [OK] Roupa")


def test_eletronico():
    e = Eletronico("Fone Bluetooth", 199.90, 12)
    assert e.garantia == 12
    assert "12 meses" in e.descricao()
    print("  [OK] Eletronico")


def test_alimento():
    a = Alimento("Chocolate", 8.50, "12/2025")
    assert a.validade == "12/2025"
    assert "12/2025" in a.descricao()
    print("  [OK] Alimento")


if __name__ == "__main__":
    print("\n--- Testbench: Produtos ---")
    test_roupa()
    test_eletronico()
    test_alimento()
    print()
