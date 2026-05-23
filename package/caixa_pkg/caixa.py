from package.carrinho_pkg.carrinho import Carrinho


class Caixa:
    def __init__(self, operador: str):
        self.operador = operador

    def finalizar_compra(self, carrinho: Carrinho):
        if not carrinho.produtos:
            print("  Carrinho vazio. Nada a finalizar.")
            return
        carrinho.listar()
        print(f"\n  Total: R$ {carrinho.total():.2f}")
        print(f"  Compra finalizada pelo operador: {self.operador}\n")
