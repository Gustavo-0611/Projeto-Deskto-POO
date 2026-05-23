from package.produtos import Roupa, Eletronico, Alimento
from package.carrinho_pkg import Carrinho
from package.caixa_pkg import Caixa


def main():
    p1 = Roupa("Camiseta", 49.90, "M")
    p2 = Roupa("Calça Jeans", 119.90, "42")
    p3 = Eletronico("Fone Bluetooth", 199.90, 12)
    p4 = Eletronico("Carregador USB", 59.90, 6)
    p5 = Alimento("Chocolate", 8.50, "12/2025")
    p6 = Alimento("Café 500g", 22.00, "06/2026")

    print("\n--- Produtos disponíveis ---")
    for p in [p1, p2, p3, p4, p5, p6]:
        print(f"  {p} | {p.descricao()}")

    print("\n--- Adicionando ao carrinho ---")
    carrinho = Carrinho()
    carrinho.adicionar(p1)
    carrinho.adicionar(p3)
    carrinho.adicionar(p5)
    carrinho.adicionar(p6)

    print("\n--- Finalizando compra ---")
    caixa = Caixa("Ana")
    caixa.finalizar_compra(carrinho)

    print("--- Removendo item ---")
    carrinho.remover("Chocolate")

    print("\n--- Nova finalização ---")
    caixa2 = Caixa("Carlos")
    caixa2.finalizar_compra(carrinho)

    print("--- Carrinho vazio ---")
    caixa.finalizar_compra(Carrinho())


if __name__ == "__main__":
    main()
