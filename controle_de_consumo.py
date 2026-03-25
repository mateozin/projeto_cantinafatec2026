from controle_de_estoque import *
from controle_de_pagamento import *

class Consumo:
    def __init__(self, pagamento, produto, quantidade):
        self.pagamento = pagamento
        self.produto = produto
        self.quantidade = quantidade

    def __str__(self):
        return f"[CONSUMO] Cliente: {self.pagamento.nome_cliente} | Valor Total: R${self.pagamento.valor} \n Realizado no dia {self.pagamento.data_hora} \n Produto comprado {self.produto} x{self.quantidade}"

class NoConsumo:
    def __init__(self, consumo):
        self.consumo = consumo
        self.proximo = None

class ListaConsumo:
    def __init__(self):
        self.inicio = None

    def listar(self):
        atual = self.inicio
        while atual:
            print(atual.consumo)
            atual = atual.proximo
