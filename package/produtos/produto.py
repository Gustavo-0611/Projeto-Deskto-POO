from abc import ABC, abstractmethod


class Produto(ABC):
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    @abstractmethod
    def descricao(self) -> str:
        pass

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f}"
