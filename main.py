from controle_de_estoque import *
from controle_de_pagamento import *
from controle_de_consumo import *
from cantina_dados import *

print(f"//Listas// \n1- Listar o consumo \n2- Listar os pagamentos \n3- Listar os produtos \n//Gerar mais dados// \n4- Realizar outra série de pagamentos e consumos \n5- Criar mais produtos \n//Utilitários// \n6- Adicionar um produto \n 6.1- Editar a quantidade de um produto\n7- Adicionar um consumo \n//Relátorios// \n8- Relátorio de Venda \n9- Relátorio de Consumo \n0 - Encerrar atividade") 
while True:
    try:
        escolha = float(input("Escolha um número: "))
    except ValueError:
        print("Isso não é um número")
        escolha = -1
    if escolha == 1:
            lista_consumo.listar()
    elif escolha == 2:
            lista_pagamentos.listar()
    elif escolha == 3:
            lista_produtos.listar()
    elif escolha == 4:
            simular_consumos(lista_produtos, lista_pagamentos, lista_consumo, 5)
    elif escolha == 5:
            gerar_produtos(lista_produtos, 8)
    elif escolha == 6:
            nome = input("Nome do produto: ")
            try:
                   preco_venda = float(input("Preço de venda: "))
            except ValueError:
                   print("Valor inválido.")
                   continue
            try:
                   preco_compra = float(input("Preço de compra: "))
            except ValueError:
                   print("Valor inválido.")
                   continue
            try:
                   quantidade = int(input("Quantidade: "))
            except ValueError:
                   print("Valor inválido. Criação cancelada.")
                   continue
            try:
                data_compra = input("Data de compra (dd/mm/aaaa): ")
                data_validade = input("Data de validade (dd/mm/aaaa): ")
            except ValueError:
                   print("Data inválida. Cancelando criação de produto.")
                   continue
            prod = Produto(nome, preco_compra, preco_venda, data_compra, data_validade, quantidade)
            lista_produtos.inserir_produto(prod)
            print(f"Produto {nome} criado com sucesso. \nPreço compra: {preco_compra} \nPreço venda: {preco_venda} \nComprado dia {data_compra} \nVence dia {data_validade} \nQuantidade: {quantidade}")
    elif escolha == 6.1:
           nome = input("Nome do produto: ")
           try:
                nova_qtd = int(input("Nova quantidade: "))
           except ValueError:
                print("Valor inválido")
                continue      
           print(lista_produtos.editar_quantidade(nome, nova_qtd)) 
    elif escolha == 7:
        nome_cliente = input("Cliente: ")
        categoria = input("Categoria: ")
        curso = input("Curso: ")

        nome_produto = input("Produto: ")
        aux = lista_produtos.inicio
        produto = None
        while aux:
            if aux.produto.nome == nome_produto:
                produto = aux.produto
                break
            aux = aux.proximo

        if not produto:
            print("Produto não encontrado.")
            continue

        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            continue

        if quantidade <= 0 or quantidade > produto.quantidade:
            print("Quantidade inválida ou estoque insuficiente.")
            continue

        data = input("Data (dd/mm/aaaa hh:mm): ")
        try:
            datetime.strptime(data, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Data inválida.")
            continue

        valor_total = produto.preco_venda * quantidade

        pagamento = Pagamento(nome_cliente, categoria, curso, valor_total, data)
        lista_pagamentos.inserir_pagamento(pagamento)

        consumo = Consumo(pagamento, nome_produto, quantidade)
        lista_consumo.inserir_consumo(consumo)

        lista_produtos.baixar_estoque(nome_produto, quantidade)

        print(f"Consumo registrado no nome de {nome_cliente} comprando {nome_produto} (Valor total: R${valor_total})")
    elif escolha == 8:
        total_vendas = 0
        total_lucro = 0
        vendas_por_produto = {}

        atual = lista_consumo.inicio

        while atual:
            consumo = atual.consumo
            nome_produto = consumo.produto
            quantidade = consumo.quantidade

            total_vendas += float(consumo.pagamento.valor)

            aux = lista_produtos.inicio
            produto_encontrado = None

            while aux:
                if aux.produto.nome == nome_produto:
                    produto_encontrado = aux.produto
                    break
                aux = aux.proximo

            if produto_encontrado:
                lucro_unitario = produto_encontrado.preco_venda - produto_encontrado.preco_compra
                total_lucro += lucro_unitario * quantidade

            vendas_por_produto[nome_produto] = vendas_por_produto.get(nome_produto, 0) + quantidade

            atual = atual.proximo

        print("\n//RELATÓRIO DE VENDAS//")
        print(f"Total em vendas: R${total_vendas:.2f}")
        print(f"Lucro total: R${total_lucro:.2f}")

        if vendas_por_produto:
            mais_vendido = None
            maior_qtd = 0

            for nome, qtd in vendas_por_produto.items():
                if qtd > maior_qtd:
                    maior_qtd = qtd
                    mais_vendido = nome

            print("\nProduto mais vendido:")
            print(f"{mais_vendido} - {maior_qtd} unidades")
        else:
            print("Nenhuma venda registrada.")
    elif escolha == 9:
        total_gasto = 0
        total_produtos = 0
        gasto_por_cliente = {}

        atual = lista_consumo.inicio

        while atual:
            consumo = atual.consumo

            valor = float(consumo.pagamento.valor)
            cliente = consumo.pagamento.nome_cliente
            quantidade = consumo.quantidade

            total_gasto += valor

            total_produtos += quantidade

            gasto_por_cliente[cliente] = gasto_por_cliente.get(cliente, 0) + valor

            atual = atual.proximo

        valor_estoque = 0
        atual_prod = lista_produtos.inicio

        while atual_prod:
            produto = atual_prod.produto
            valor_estoque += produto.preco_venda * produto.quantidade
            atual_prod = atual_prod.proximo

        print("\n//RELATÓRIO DE CONSUMO//")
        print(f"Total gasto em produtos do estoque: R${total_gasto:.2f}")
        print(f"Total de produtos consumidos: {total_produtos}")
        print(f"Valor potencial do estoque: R${valor_estoque:.2f}")

        if gasto_por_cliente:
            cliente_top = max(gasto_por_cliente, key=gasto_por_cliente.get)
            print(f"Cliente que mais gastou: {cliente_top} (R${gasto_por_cliente[cliente_top]:.2f})")
        else:
            print("Nenhum consumo registrado.")
    elif escolha == 0:
        print("Encerrando...")
        break
    else:
        print("Escolha inválida")