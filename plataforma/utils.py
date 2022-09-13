import re, random
from django.contrib import messages
from django.contrib.messages import constants
from plataforma.models import Cliente, Pedido, Veiculos
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image
import datetime


def validar_dados(request, email, cpf, telefone):
    if not re.search('[\w]+@[\w]+\.com[\.\w]{0,5}', email):
        messages.add_message(request, constants.ERROR, 'Email inválido')
        return False

    if not re.search('[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}', cpf):
        messages.add_message(request, constants.ERROR, 'Favor usar o formato xxx.xxx.xxx-xx no campo "CPF"')
        return False

    if not re.search('[0-9]{8,12}', telefone):
        messages.add_message(request, constants.ERROR, 'Telefone inválido')
        return False

    if Cliente.objects.filter(cpf=cpf).exists():
        messages.add_message(request, constants.ERROR, 'CPF já existe')
        return False

    if Cliente.objects.filter(email=email).exists():
        messages.add_message(request, constants.ERROR, 'Email já existe')
        return False

    return True

def validar_placa(request, placa):
    if Veiculos.objects.filter(placa=placa).exists():
        messages.add_message(request, constants.ERROR, 'Placa já existe')
        return False

    if not re.search('[\w]{3,4}-{0,1}[\w]{4,5}', placa):
        messages.add_message(request, constants.ERROR, 'Placa inválida')
        return False

    return True

def criar_os(request):
    temp = random.randint(0, 99999999)

    while Pedido.objects.filter(ods=temp).exists():
        temp = random.randint(0, 99999999)

    return temp

def validar_pedido(request, descricao, preco, ods):
    if len(descricao.strip()) == 0  or len(ods.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return False

    if re.search('[a-bA-B]', preco):
        messages.add_message(request, constants.ERROR, 'Insira um preço válido ou deixe vazio')
        return False

    if len(descricao) >= 256:
        messages.add_message(request, constants.ERROR, 'Descricao muito grande')
        return False

    return True

def validar_preco(request, preco):
    if len(preco) == 0 or len(preco.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Insira um preco válido')
        return False

    return True

def validar_descricao(request, descricao):
    if len(descricao) == 0 or len(descricao.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Insira uma descrição válida')
        return False

    return True

titulo = 'LavaTlias'

class PDF(FPDF):

    def header(self):

        self.image("./media/img_pdf/TliasImg.png", 10, 8, 20)

        self.set_font("helvetica", "B", 15)

        width = self.get_string_width(titulo) + 10
        doc_w = self.w
        self.set_x((doc_w - width) / 2)
        self.cell(
            width, 9,
            titulo,
            border=1,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
            align="C",
            fill=False,
        )

        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def gerar_pdf(request, ods):

    pedido = Pedido.objects.filter(ods=ods).first()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin = 15)
    pdf.add_page()

    pdf.set_font("helvetica", "B", size=15)
    pdf.cell(20, 8, '_______________________________________________________________', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(0, 8, f'Cliente: {pedido.veiculo.cliente}, CPF: {pedido.veiculo.cliente.cpf}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(0, 8, f'Contato: {pedido.veiculo.cliente.email}  -  {pedido.veiculo.cliente.telefone}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, '_______________________________________________________________', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, f'Veiculo: {pedido.veiculo} {pedido.veiculo.ano} - {pedido.veiculo.marca}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.ln(15)
    pdf.image(f"./{pedido.veiculo.imagem.url}", w=200, h=100)
    pdf.ln(15)
    pdf.cell(20, 8, f'Placa: {pedido.veiculo.placa}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, '_______________________________________________________________', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.ln(100)
    pdf.cell(20, 8, f'Descrição: {pedido.descricao}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, f'Data de inicio do pedido: {pedido.data_abertura.strftime("%d/%m/%Y %H:%M")}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, f'Data de termino: {pedido.data_finalizacao.strftime("%d/%m/%Y %H:%M")}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.ln(15)
    pdf.cell(20, 8, f'Ordem de serviço: {pedido.ods}', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, f'Valor: R$ {pedido.preco}0', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.cell(20, 8, '_______________________________________________________________', new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.image(f"./{pedido.imagem_final.url}", w=200, h=100)

    pdf.output("teste.pdf")

    return True

def trocar_img(request, id_cliente):

    temp = acessar_antes()

    pessoa = Cliente.objects.filter(id=id_cliente).first()
    veiculos_depois = Veiculos.objects.filter(cliente=pessoa.id).all()
    
    unica_url = []

    if temp == False:

        url = [veiculos_depois[0].imagem.url]
        repor_imagem(url)

        return

    else:
        for i in veiculos_depois:
            unica_url.append(i.imagem.url)

        for i in temp:
            if i in unica_url:
                unica_url.remove(i)
                
        repor_imagem(unica_url)

        return

def anotacao_de_antes(request, veiculos_antes):
    with open('./media/img/save.txt', 'w') as arq:
        for i in veiculos_antes:
            arq.writelines(f'{i.imagem.url}\n')

    return

def acessar_antes():
    with open('./media/img/save.txt', 'r') as arq:
        temp = arq.readlines()
        if len(temp) == 0:
            return False
        else:
            temp = list(map(lambda x: x.replace('\n', ''), temp))

    return temp

def repor_imagem(url):

    logo_url = './media/img_pdf/TliasImg.png'

    print(url)

    imagem_url = url[0]

    print(url)

    logo = Image.open(logo_url)

    imagem = Image.open(f'.{imagem_url}')

    nova_imagem = imagem.resize((1280, 720))

    cords = ((nova_imagem.width - logo.width), (nova_imagem.height - logo.height))

    nova_imagem.paste(logo, cords)
    nova_imagem.save(f'.{imagem_url}')