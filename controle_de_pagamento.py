from datetime import datetime

class Pagamento:
    def __init__(self, nome, categoria, curso, valor, data_hora):
        categorias_permitidas = ["aluno", "servidor", "professor"]
        cursos_permitidos = ["IA", "ESG"]
        if categoria not in categorias_permitidas:
            raise ValueError("Categoria inválida, use apenas aluno, servidor ou professor!")
        if curso not in cursos_permitidos:
            raise ValueError("Curso inválido, use apenas IA ou ESG!")
        self.nome = nome
        self.categoria = categoria
        self.curso = curso
        self.valor = valor
        self.data_hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M")

    def __str__(self):
        return f"Nome: {self.nome} \nCategoria: {self.categoria} \nCurso: {self.curso} \nValor: R${self.valor} \nData e Hora da compra: {self.data_hora}"

class NoPagamento:
    def __init__(self, pagamento):
        self.pagamento = pagamento
        self.proximo = None

class ListaPagamentos:
    def __init__(self):
        self.inicio = None

    def inserir_pagamento(self, pagamento):
        novo = NoPagamento(pagamento)

        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo

    def listar(self):
        atual = self.inicio
        while atual:
            print(atual.pagamento)
            atual = atual.proximo
