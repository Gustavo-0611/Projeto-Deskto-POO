from package.produtos.produto import Produto


class Roupa(Produto):
    def __init__(self, nome: str, preco: float, tamanho: str):
        super().__init__(nome, preco)
        self.tamanho = tamanho

    def descricao(self) -> str:
        return f"Roupa | Tamanho: {self.tamanho}"


class Eletronico(Produto):
    def __init__(self, nome: str, preco: float, garantia: int):
        super().__init__(nome, preco)
        self.garantia = garantia

    def descricao(self) -> str:
        return f"Eletrônico | Garantia: {self.garantia} meses"


class Alimento(Produto):
    def __init__(self, nome: str, preco: float, validade: str):
        super().__init__(nome, preco)
        self.validade = validade

    def descricao(self) -> str:
        return f"Alimento | Validade: {self.validade}"
