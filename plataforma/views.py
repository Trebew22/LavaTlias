from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Pedido, Veiculos
from .utils import anotacao_de_antes, trocar_img, validar_dados, validar_placa, criar_os, validar_pedido, validar_preco, validar_descricao, gerar_pdf as pdf
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime


def home(request):
    if request.method == 'GET':

        pedido = Pedido.objects.all()

        return render(request, 'home.html', {'pedido': pedido})

    if request.method == 'POST':
        ods = request.POST.get('ods')

        if len(ods) == 0 or len(ods.strip()) == 0:
            redirect('/home')
        
        pedido = Pedido.objects.filter(ods=ods).first()

        return redirect(f'/consulta_unica/{pedido.ods}')

def adicionar_cliente(request):
    if request.method == 'GET':
        return render(request, 'cadastro/cadastro.html')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')

        telefone = request.POST.get('telefone')

        if not validar_dados(request, email, cpf, telefone):
            return redirect('/adicionar_cliente')


        try:
            cliente = Cliente(nome = nome,
                            cpf = cpf,
                            email = email,
                            telefone = telefone)

            cliente.save()

            messages.add_message(request, constants.SUCCESS, 'Cadastro feito com sucesso')
            
            return redirect('/cadastro_veiculo')
            
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/adicionar_cliente')

def cadastro_veiculo(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all().order_by('nome')
        return render(request, 'cadastroV/cadastro_veiculo.html', {'clientes':clientes})

    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        ano = request.POST.get('ano')
        placa = request.POST.get('placa')
        id_cliente = request.POST.get('dono_veiculo')
        img = request.FILES.get('imagem')

        pessoa = Cliente.objects.filter(id=id_cliente).first()

        if not validar_placa(request, placa):
            return redirect('/cadastro_veiculo')

        veiculos_antes = Veiculos.objects.filter(cliente=pessoa.id)

        anotacao_de_antes(request, veiculos_antes)

        try:
            veiculo = Veiculos(
                modelo=modelo,
                marca=marca,
                ano=ano,
                placa=placa,
                cliente=pessoa,
                imagem = img
            )

            veiculo.save()

            trocar_img(request, id_cliente)

            messages.add_message(request, constants.SUCCESS, 'Cadastro feito com sucesso')
            return redirect('/cadastro_pedido')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/cadastro_veiculo')

def cadastro_pedido(request):
    if request.method == 'GET':
        veiculos = Veiculos.objects.all()
        ods = criar_os(request)

        return render(request, 'cadastroP/cadastro_pedido.html', {'veiculos':veiculos,
                                                                    'ods':ods,})

    elif request.method == 'POST':
        servico = request.POST.get('servico')
        descricao = request.POST.get('descricao')
        veiculo = request.POST.get('veiculo')
        preco = request.POST.get('preco')
        ods = request.POST.get('ods')

        veiculo_query = Veiculos.objects.filter(modelo=veiculo).first()

        try:
            if not validar_pedido(request, descricao, preco, ods):
                return redirect('/cadastro_pedido')

            if len(preco) == 0:
                preco = 0
                preco = float(preco)

            if servico == 'M':

                pedido = Pedido(
                            servicos=servico,
                            descricao=descricao,
                            veiculo=veiculo_query,
                            data_abertura=datetime.now(),
                            preco=preco,
                            ods=ods,
                            combinar_preco=True
                            )
            
                pedido.save()

                messages.add_message(request, constants.SUCCESS, 'Cadastro feito com sucesso')
                return redirect(f'/consulta_unica/{ods}')

            if servico == 'L':

                pedido = Pedido(
                            servicos=servico,
                            descricao=descricao,
                            veiculo=veiculo_query,
                            data_abertura=datetime.now(),
                            preco=40.00,
                            ods=ods,
                            )
            
                pedido.save()

                messages.add_message(request, constants.SUCCESS, 'Cadastro feito com sucesso')
                return redirect(f'/consulta_unica/{ods}')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/cadastro_pedido')

def consultar(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all().order_by('-data_abertura')

        return render(request, 'consultar.html', {'pedidos':pedidos})

def consulta_unica(request, ods):

    pedidos = Pedido.objects.filter(ods=ods)

    return render(request, 'consulta_unica.html', {'pedidos':pedidos})

def ajustar(request, ods):

    if request.method == 'POST':
        preco_ajuste = request.POST.get('preco')
        descricao_ajuste = request.POST.get('descricao')
        imagem_final = request.FILES.get('imagem')

        if imagem_final == None:
            messages.add_message(request, constants.ERROR, 'Insira uma imagem válida')
            return redirect('/consultar')

        if not validar_descricao(request, descricao_ajuste):
            return redirect('/consultar')

        if not validar_preco(request, preco_ajuste):
            return redirect('/consultar')

        ajustar_pedido = Pedido.objects.filter(ods=ods).first()
        query_veiculo = Veiculos.objects.filter(ods=ods)

        print(query_veiculo.veiculo)

        if len(descricao_ajuste.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Insira uma descrição válida')
            return redirect('/consultar')

        #print(ajustar_pedido.veiculo.imagem.url)

        #anotacao_de_antes(request, veiculos_antes)

        #try:
        ajustar_pedido.preco = preco_ajuste
        ajustar_pedido.combinar_preco = False
        ajustar_pedido.flag_ativo = False
        ajustar_pedido.descricao = descricao_ajuste
        ajustar_pedido.imagem_final = imagem_final
        ajustar_pedido.data_finalizacao = datetime.now()

        #ajustar_pedido.save()
        
        messages.add_message(request, constants.SUCCESS, 'Pedido alterado com sucesso')
        return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

        # except:
        #     messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
        #     return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

def ajustar_lav(request, ods):
    if request.method == 'POST':
        imagem_final = request.FILES.get('imagem')

        ajustar_pedido = Pedido.objects.filter(ods=ods).first()

        if imagem_final == None:
            messages.add_message(request, constants.ERROR, 'Insira uma imagem válida')
            return redirect('/consultar')

        try:
            ajustar_pedido.imagem_final = imagem_final
            ajustar_pedido.flag_ativo = False
            ajustar_pedido.data_finalizacao = datetime.now()

            ajustar_pedido.save()

            messages.add_message(request, constants.SUCCESS, 'Pedido alterado com sucesso')
            return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

def gerar_pdf(request, ods):

    pdf(request, ods)

    return redirect(f'/consulta_unica/{ods}')