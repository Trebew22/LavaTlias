from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pedido, Veiculos
from . import utils #verf_cpf1, verf_email1, verf_ano, verf_marca, verf_modelo, verf_placa ,verf_cpf, verf_email, verf_nome, verf_placa1, verf_telefone, editar_imagem, criar_os, validar_pedido, validar_preco, validar_descricao, gerar_pdf as pdf
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.transaction import atomic

def home(request):
    if request.method == 'GET':

        pedido = Pedido.objects.all()

        return render(request, 'home.html', {'pedido': pedido})

    if request.method == 'POST':
        ods = request.POST.get('ods')
        
        if not Pedido.objects.filter(ods=ods).exists():
            messages.add_message(request, constants.WARNING, 'Ordem de serviço inválida')
            return redirect('/home')

        pedido = Pedido.objects.filter(ods=ods).first()
    
        return redirect(f'/consulta_unica/{pedido.ods}')

def cadastro_cliente(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        return render(request, 'cadastro/cadastro.html', {'clientes': clientes})

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        modelo = request.POST.getlist('modelo')
        marca = request.POST.getlist('marca')
        ano = request.POST.getlist('ano')
        placa = request.POST.getlist('placa')
        img = request.FILES.getlist('imagem')

        clientes = Cliente.objects.all()

        if not utils.verf_cpf1(request, cpf):
            return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

        if not utils.verf_nome(request, nome):
           return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'cpf': cpf, 'email': email, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

        if not utils.verf_email1(request, email):
            return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

        if not utils.verf_telefone(request, telefone):
            return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'veiculos': zip(modelo, marca, ano, placa)})
        
        try:
            cliente = Cliente(nome = nome,
                            cpf = cpf,
                            email = email,
                            telefone = telefone)

            for i in modelo:
                if not utils.verf_modelo(request, i):
                    return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

            for i in marca:
                if not utils.verf_marca(request, i):
                    return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

            for i in ano:
                if not utils.verf_ano(request, i):
                    return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

            for i in placa:
                if not utils.verf_placa1(request, i):
                    return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})
            
            if len(modelo) >= 1 or len(marca) >= 1 or len(ano) >= 1 or len(placa) >= 1:
                if len(img) == 0:
                        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, adicione uma imagem do veiculo')
                        return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

            for i in img:
                if i.size > 20000000:
                    messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique o tamanho da imagem')
                    return render(request, 'cadastro/cadastro.html', {'clientes': clientes, 'nome': nome, 'email': email, 'cpf': cpf, 'telefone': telefone, 'veiculos': zip(modelo, marca, ano, placa)})

            cliente.save()

            for modelo, marca, ano, placa, img in zip(modelo, marca, ano, placa, img):

                img_editada = utils.editar_imagem(img)

                veiculo = Veiculos(modelo = modelo,
                                    marca = marca,
                                    ano = ano,
                                    placa = placa,
                                    cliente = cliente,
                                    imagem = img_editada,
                                    imagem_original = img)

                veiculo.save()

            messages.add_message(request, constants.SUCCESS, 'Cadastro do Cliente feito com sucesso')
            return redirect('/cadastro_cliente')
            
        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/cadastro_cliente')

def excluir_veiculo(request, id):
    try:
        veiculo = Veiculos.objects.get(id=id)
        veiculo.delete()
        return True

    except:
        messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
        return redirect('/cadastro_cliente')

def att(request):
    
    id_cliente = request.POST.get('id_cliente')
    
    cliente = Cliente.objects.filter(id=id_cliente)
    veiculos = Veiculos.objects.filter(cliente=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    veiculos_json = json.loads(serializers.serialize('json', veiculos))

    veiculos_json = [{'id': veiculo['pk'], 'veiculo': veiculo['fields']} for veiculo in veiculos_json]

    data = {'cliente': cliente_json, 'id':id_cliente, 'veiculos': veiculos_json}

    return JsonResponse(data)

@csrf_exempt
@atomic
def att_cliente(request):

    if request.method == 'POST':

        rm_car_id = request.POST.getlist('rm_car')
        
        if rm_car_id:
                for i in rm_car_id:
                    excluir_veiculo(request, i)
        
        cliente_id = request.POST.get('cliente_id')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

        print(cpf)

        modelo = request.POST.getlist('modelo')
        marca = request.POST.getlist('marca')
        ano = request.POST.getlist('ano')
        placa = request.POST.getlist('placa')
        veiculo_id = request.POST.getlist('car_id')

        lista_carros = list(zip(modelo, marca, ano, placa, veiculo_id))

        cliente = Cliente.objects.get(id=cliente_id)

        for i in lista_carros:
            modelo = i[0]
            marca = i[1]
            ano = i[2]
            placa = i[3]
            veiculo_id = i[4]
            
            veiculo = Veiculos.objects.get(id=veiculo_id)

            try:

                if not utils.verf_placa(request, placa, veiculo_id):
                    return redirect('/cadastro_cliente')

                if not utils.verf_modelo(request, modelo):
                    return redirect('/cadastro_cliente')

                if not utils.verf_marca(request, marca):
                    return redirect('/cadastro_cliente')

                if not utils.verf_ano(request, ano):
                    return redirect('/cadastro_cliente')

                veiculo.modelo = modelo
                veiculo.marca = marca
                veiculo.ano = ano
                veiculo.placa = placa

                veiculo.save()

            except Exception as e:
                print(e)
                messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
                return redirect('/cadastro_cliente')

        clientes = Cliente.objects.all()

        try:
            
            if cliente.nome != nome:
                if not utils.verf_nome(request, nome):
                    return render(request, 'cadastro/cadastro.html', {'clientes':clientes})

            if cliente.cpf != cpf:
                if not utils.verf_cpf(request, cpf, cliente_id):
                    return render(request, 'cadastro/cadastro.html', {'clientes':clientes})

            if cliente.email != email:
                if not utils.verf_email(request, email):
                    return render(request, 'cadastro/cadastro.html', {'clientes':clientes})
            
            if cliente.telefone != telefone:
                if not utils.verf_telefone(request, telefone):
                    return render(request, 'cadastro/cadastro.html', {'clientes':clientes})
            
            cliente.nome = nome
            cliente.email = email
            cliente.cpf = cpf
            cliente.telefone = telefone

            cliente.save()
            
            messages.add_message(request, constants.SUCCESS, 'Cliente atualizado com sucesso')
            return redirect('/cadastro_cliente')

        except Exception as e:
            print(e)
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/cadastro_cliente')

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

        pessoa = Cliente.objects.get(id=id_cliente)

        if img.size > 20000000:
            messages.add_message(request, constants.SUCCESS, 'Arquivo muito pesado')
            return redirect('/cadastro_veiculo')

        if not utils.verf_placa1(request, placa):
            return redirect('/cadastro_veiculo')

        try:

            imagem_editada = utils.editar_imagem(img)
            
            veiculo = Veiculos(
                modelo=modelo,
                marca=marca,
                ano=ano,
                placa=placa,
                cliente=pessoa,
                imagem=imagem_editada,
                imagem_original = img,
            )

            veiculo.save()

            messages.add_message(request, constants.SUCCESS, 'Cadastro feito com sucesso')
            return redirect('/cadastro_pedido')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/cadastro_veiculo')

def cadastro_pedido(request):
    if request.method == 'GET':
        veiculos = Veiculos.objects.all()

        ods = utils.criar_os(request)

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
            if not utils.validar_pedido(request, descricao, preco, ods):
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

def ajustar(request):

    if request.method == 'POST':
        preco_ajuste = request.POST.get('preco')
        descricao_ajuste = request.POST.get('descricao')
        imagem_final = request.FILES.get('imagem')
        ods = request.POST.get('ods')

        if imagem_final == None:
            messages.add_message(request, constants.ERROR, 'Insira uma imagem válida')
            return redirect('/consultar')

        if not utils.validar_descricao(request, descricao_ajuste):
            return redirect('/consultar')

        if not utils.validar_preco(request, preco_ajuste):
            return redirect('/consultar')

        ajustar_pedido = Pedido.objects.get(ods=ods)

        if len(descricao_ajuste.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Insira uma descrição válida')
            return redirect('/consultar')

        try:
            ajustar_pedido.preco = preco_ajuste
            ajustar_pedido.combinar_preco = False
            ajustar_pedido.flag_ativo = False
            ajustar_pedido.descricao = descricao_ajuste
            ajustar_pedido.imagem_final = imagem_final
            ajustar_pedido.data_finalizacao = datetime.now()

            ajustar_pedido.save()
            
            messages.add_message(request, constants.SUCCESS, 'Pedido alterado com sucesso')
            return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect(f'/consulta_unica/{ajustar_pedido.ods}')

def ajustar_lav(request):
    if request.method == 'POST':
        imagem_final = request.FILES.get('imagem')
        ods = request.POST.get('ods')

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

    utils.gerar_pdf(request, ods)

    return redirect(f'/consulta_unica/{ods}')

def enviar_email(request, ods):

    servico = Pedido.objects.filter(ods=ods).first()

    html_content = render_to_string('emails/email_clientes.html', {'servico':servico})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives('Serviço concluido', text_content, 'lavatlias@email.com', ['clientes@gmail.com'])
    email.attach_alternative(html_content, 'text/html')
    email.send()

    messages.add_message(request, constants.SUCCESS, 'Email enviado com sucesso')
    return redirect(f'/consulta_unica/{ods}')