from controle_de_estoque import *
from controle_de_pagamento import *
from controle_de_consumo import *
from faker import Faker
import random
import pickle

fake = Faker("pt_BR")

def gerar_produtos(lista_produtos, n=10):
    nomes_usados = set()

    while len(nomes_usados) < n:
        nomes_usados.add(fake.word().capitalize())

    for nome in nomes_usados:
        preco_venda = random.randint(1, 18)
        preco_compra = round(preco_venda * 0.6, 2)

        data_compra = fake.date_this_year().strftime("%d/%m/%Y")
        data_validade = fake.date_between(start_date="today", end_date="+30d").strftime("%d/%m/%Y")

        quantidade = random.randint(10, 50)

        produto = Produto(nome, preco_compra, preco_venda, data_compra, data_validade, quantidade)
        lista_produtos.inserir_produto(produto)

def simular_consumos(lista_produtos, lista_pagamentos, lista_consumo, n=10):
    categorias = ["aluno", "servidor", "professor"]
    cursos = ["IA", "ESG"]

    atual = lista_produtos.inicio
    produtos = []

    while atual:
        produtos.append(atual.produto)
        atual = atual.proximo

    for _ in range(n):
        if not produtos:
            break

        produto = random.choice(produtos)

        if produto.quantidade <= 0:
            continue

        quantidade = random.randint(1, min(10, produto.quantidade))

        nome = fake.name()
        categoria = random.choice(categorias)
        curso = random.choice(cursos)

        valor_total = produto.preco_venda * quantidade
        data = fake.date_time_this_year().strftime("%d/%m/%Y %H:%M")

        if lista_produtos.baixar_estoque(produto.nome, quantidade):

            valor_total = produto.preco_venda * quantidade

            pagamento = Pagamento(nome, categoria, curso, valor_total, data)
            lista_pagamentos.inserir_pagamento(pagamento)

            consumo = Consumo(pagamento, produto.nome, quantidade)

            novo = NoConsumo(consumo)
            if lista_consumo.inicio is None:
                lista_consumo.inicio = novo
            else:
                aux = lista_consumo.inicio
                while aux.proximo:
                    aux = aux.proximo
                aux.proximo = novo   

def salvar(nome, objeto):
    with open(nome, "wb") as f:
        pickle.dump(objeto, f)

def carregar(nome):
    try:
        with open(nome, "rb") as f:
            return pickle.load(f)
    except:
        return None

lista_produtos = carregar("produtos.pkl") or ListaProdutos()
lista_pagamentos = carregar("pagamentos.pkl") or ListaPagamentos()
lista_consumo = carregar("consumo.pkl") or ListaConsumo()
gerar_produtos(lista_produtos, 8)
simular_consumos(lista_produtos, lista_pagamentos, lista_consumo, 5)