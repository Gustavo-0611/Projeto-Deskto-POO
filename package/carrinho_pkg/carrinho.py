from package.produtos.produto import Produto


class Carrinho:
    def __init__(self):
        self._produtos: list[Produto] = []

    def adicionar(self, produto: Produto):
        self._produtos.append(produto)
        print(f"  '{produto.nome}' adicionado ao carrinho.")

    def remover(self, nome: str):
        for p in self._produtos:
            if p.nome.lower() == nome.lower():
                self._produtos.remove(p)
                print(f"  '{nome}' removido do carrinho.")
                return
        print(f"  '{nome}' não encontrado no carrinho.")

    def listar(self):
        if not self._produtos:
            print("  Carrinho vazio.")
            return
        print(f"\n  Carrinho ({len(self._produtos)} item(s)):")
        print("  " + "-" * 38)
        for i, p in enumerate(self._produtos, 1):
            print(f"  {i}. {p} | {p.descricao()}")

    def total(self) -> float:
        return sum(p.preco for p in self._produtos)

    @property
    def produtos(self):
        return self._produtos
