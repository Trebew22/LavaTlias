import re, random, os, sys
from django.contrib import messages
from django.contrib.messages import constants
from plataforma.models import Cliente, Pedido, Veiculos
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from django.conf import settings
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from lavajato.settings import BASE_DIR

def verf_nome(request, nome):
    if len(nome.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Nome não pode estar vazio')
            return False

    return True

def verf_cpf(request, cpf, id_cliente):
    list_cpf = Cliente.objects.filter(cpf=cpf).exclude(id=id_cliente)

    if list_cpf.exists():
        messages.add_message(request, constants.ERROR, 'CPF já existente')
        return False

    if not re.search('[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}', cpf):
        messages.add_message(request, constants.ERROR, 'Favor usar o formato xxx.xxx.xxx-xx no campo "CPF"')
        return False

    return True

def verf_cpf1(request, cpf):

    if Cliente.objects.filter(cpf=cpf).exists():
        messages.add_message(request, constants.ERROR, 'CPF já existente')
        return False

    if not re.search('[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}', cpf):
        messages.add_message(request, constants.ERROR, 'Favor usar o formato xxx.xxx.xxx-xx no campo "CPF"')
        return False

    return True

def verf_email(request, email, id_cliente):
    list_email = Cliente.objects.filter(email=email).exclude(id=id_cliente)

    if not re.search('[\w]+@[\w]+\.com[\.\w]{0,5}', email):
        messages.add_message(request, constants.ERROR, 'Email inválido')
        return False

    if list_email.exists():
        messages.add_message(request, constants.ERROR, 'Email já existe')
        return False

    return True

def verf_email1(request, email):

    if not re.search('[\w]+@[\w]+\.com[\.\w]{0,5}', email):
        messages.add_message(request, constants.ERROR, 'Email inválido')
        return False

    if Cliente.objects.filter(email=email).exists():
        messages.add_message(request, constants.ERROR, 'Email já existe')
        return False

    return True

def verf_telefone(request, telefone):
    if not re.search('[0-9]{8,12}', telefone):
        messages.add_message(request, constants.ERROR, 'Telefone inválido')
        return False

    if len(telefone) >= 11:
        messages.add_message(request, constants.ERROR, 'Telefone inválido')
        return False

    return True

def verf_modelo(request, modelo):
    if len(modelo.strip()) == 0:
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, Modelo não pode estar vazio')
        return False

    return True

def verf_marca(request, marca):
    if len(marca.strip()) == 0:
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, Marca não pode estar vazio')
        return False

    return True

def verf_ano(request, ano):
    if len(ano.strip()) == 0:
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, Ano não pode ser vazio')
        return False

    if not ano.isdigit():
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, Ano precisa ser numeros')
        return False

    return True

def verf_placa(request, placa, id_cliente):
    list_placas = Veiculos.objects.filter(placa=placa).exclude(id=id_cliente)

    if list_placas.exists():
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique a placa')
        return False

    if not re.search('[\w]{3,4}-{0,1}[\w]{4,5}', placa):
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique a placa')
        return False

    return True

def verf_placa1(request, placa):

    if Veiculos.objects.filter(placa=placa).exists():
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique a placa')
        return False

    if not re.search('[\w]{3,4}-{0,1}[\w]{4,5}', placa):
        messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique a placa')
        return False

    return True

# def verf_img(request, img):
#     print(img)
#     print(type(img))
#     if img.size > 20000000:
#         messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, verifique o tamanho da imagem')
#         return False

#     if len(img) == 0:
#         messages.add_message(request, constants.WARNING, 'Falha ao cadastrar o Veiculo, adicione uma imagem do veiculo')
#         return False

#     return True

# def validar_dados(request, email, cpf, telefone, nome):

#     if Cliente.objects.filter(cpf=cpf).exists():
#         messages.add_message(request, constants.ERROR, 'CPF já existente')
#         return render(request, 'cadastro/cadastro.html', {'nome': nome, 'email': email, 'telefone': telefone})

#     if not re.search('[\w]+@[\w]+\.com[\.\w]{0,5}', email):
#         messages.add_message(request, constants.ERROR, 'Email inválido')
#         return render(request, 'cadastro/cadastro.html', {'nome': nome, 'cpf': cpf, 'telefone': telefone})

#     if not re.search('[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}', cpf):
#         messages.add_message(request, constants.ERROR, 'Favor usar o formato xxx.xxx.xxx-xx no campo "CPF"')
#         return render(request, 'cadastro/cadastro.html', {'nome': nome, 'email': email, 'telefone': telefone})

#     if not re.search('[0-9]{8,12}', telefone):
#         messages.add_message(request, constants.ERROR, 'Telefone inválido')
#         return render(request, 'cadastro/cadastro.html', {'nome': nome, 'email': email, 'cpf': cpf})

#     if not Cliente.objects.filter(email=email).exists():
#         messages.add_message(request, constants.ERROR, 'Email já existe')
#         return render(request, 'cadastro/cadastro.html', {'nome': nome, 'cpf': cpf, 'telefone': telefone})

#     return 

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

class PDF(FPDF):

    def header(self):

        titulo = 'LavaTlias'

        self.image("./media/pdf/TliasImg.png", 10, 8, 20)

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
    pdf.image(f".{pedido.veiculo.imagem.url}", w=200, h=100)
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

    nome = f'{pedido.ods}-{date.today()}'

    path = os.path.join(settings.MEDIA_ROOT, f'pdf/{nome}.pdf')

    pdf.output(path)

    return True

def editar_imagem(img):

    nome_imagem = img.name
            
    nome = f'{date.today()}-{nome_imagem}'
    
    img_aux = Image.open(img)
    img_aux = img_aux.convert('RGB')
    img_aux = img_aux.resize((1024, 720))

    path = os.path.join(BASE_DIR, 'templates/static/fontes/arial_narrow_7.ttf')

    fonte = ImageFont.truetype(path, 25)

    draw = ImageDraw.Draw(img_aux)
    draw.text((1, 600), f"Tlias {date.today()}", (255, 255, 255), font=fonte)

    saida = BytesIO()

    img_aux.save(saida, format="JPEG", quality=100)

    saida.seek(0)

    return InMemoryUploadedFile(saida, "ImageField", nome, "image/jpeg", sys.getsizeof(saida), None)