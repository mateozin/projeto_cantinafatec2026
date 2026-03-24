from datetime import datetime

class Produto:
    def __init__(self, nome, preco_compra, preco_venda, data_compra, data_validade, quantidade):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.data_compra = datetime.strptime(data_compra, "%d/%m/%Y")
        self.data_validade = datetime.strptime(data_validade, "%d/%m/%Y")   
        self.quantidade = quantidade

    def __str__(self):
        return f"Produto: {self.nome} \nPreço de compra: R${self.preco_compra} \nPreço de venda: R${self.preco_venda} \nQuantidade: {self.quantidade} \nComprado no dia: {self.data_compra.date()} \nValidade: {self.data_validade.date()}"

class No:
    def __init__(self, produto):
        self.produto = produto
        self.proximo = None

class ListaProdutos:
    def __init__(self):
        self.inicio = None
    
    def existente(self, produto):
        atual = self.inicio
        while atual:
            if (atual.produto.nome == produto.nome and 
                atual.produto.data_validade == produto.data_validade):
                return atual
            atual = atual.proximo
        return None

    def inserir_produto(self, produto):
        existe = self.existente(produto)

        if existe:
            existe.produto.quantidade += produto.quantidade
            return f"O produto já existe, quantidade adicionada ao estoque de {produto.nome}."
        novo_no = No(produto)

        if self.inicio is None or produto.data_validade < self.inicio.produto.data_validade: 
            novo_no.proximo = self.inicio
            self.inicio = novo_no
            return

        atual = self.inicio
        while atual.proximo and atual.proximo.produto.data_validade <= produto.data_validade:
            atual = atual.proximo

        novo_no.proximo = atual.proximo
        atual.proximo = novo_no
    
    def listar(self):
        atual = self.inicio
        while atual:
            print(atual.produto)
            atual = atual.proximo
    
    def editar_quantidade(self, nome, nova_quantidade):
        atual = self.inicio
        while atual:
            if atual.produto.nome == nome:
                atual.produto.quantidade = nova_quantidade
                return f"Editando a quantidade para {nova_quantidade} do estoque de {nome}"
            atual = atual.proximo
        return f"Produto não encontrado"
    
    def adicionar_quantidade(self, nome, add_quantidade):
        if add_quantidade <= 0:
            return f"Quantidade inválida"
        atual = self.inicio
        while atual:
            if atual.produto.nome == nome:
                atual.produto.quantidade += add_quantidade
                return f"Adicionando +{add_quantidade} para o estoque de {nome}"
            atual = atual.proximo
        return f"Produto não encontrado"