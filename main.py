from package.produtos import Roupa, Eletronico, Alimento
from package.carrinho_pkg import Carrinho
from package.caixa_pkg import Caixa

carrinho = Carrinho()


def menu_produtos():
    while True:
        print("\n--- Produtos ---")
        print("1. Adicionar Roupa")
        print("2. Adicionar Eletronico")
        print("3. Adicionar Alimento")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            nome = input("Nome: ")
            preco = float(input("Preco: "))
            tamanho = input("Tamanho (P/M/G): ")
            carrinho.adicionar(Roupa(nome, preco, tamanho))

        elif op == "2":
            nome = input("Nome: ")
            preco = float(input("Preco: "))
            garantia = int(input("Garantia (meses): "))
            carrinho.adicionar(Eletronico(nome, preco, garantia))

        elif op == "3":
            nome = input("Nome: ")
            preco = float(input("Preco: "))
            validade = input("Validade (MM/AAAA): ")
            carrinho.adicionar(Alimento(nome, preco, validade))

        elif op == "0":
            break
        else:
            print("Opcao invalida.")


def menu_carrinho():
    while True:
        print("\n--- Carrinho ---")
        print("1. Ver carrinho")
        print("2. Remover produto")
        print("3. Ver total")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            carrinho.listar()

        elif op == "2":
            nome = input("Nome do produto a remover: ")
            carrinho.remover(nome)

        elif op == "3":
            print(f"\n  Total: R$ {carrinho.total():.2f}")

        elif op == "0":
            break
        else:
            print("Opcao invalida.")


def menu_caixa():
    while True:
        print("\n--- Caixa ---")
        print("1. Finalizar compra")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            operador = input("Nome do operador: ")
            caixa = Caixa(operador)
            caixa.finalizar_compra(carrinho)
            carrinho._produtos.clear()
            print("  Carrinho esvaziado apos compra.")

        elif op == "0":
            break
        else:
            print("Opcao invalida.")


def main():
    while True:
        print("\n=============================")
        print("  Sistema de Loja de Produtos")
        print("=============================")
        print("1. Produtos")
        print("2. Carrinho")
        print("3. Caixa")
        print("0. Sair")
        op = input("Opcao: ").strip()

        if op == "1":
            menu_produtos()
        elif op == "2":
            menu_carrinho()
        elif op == "3":
            menu_caixa()
        elif op == "0":
            print("\nEncerrando o sistema. Ate logo!")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
