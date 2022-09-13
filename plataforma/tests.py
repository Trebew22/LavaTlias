from PIL import Image
import requests

logo_url = './media/img_pdf/TliasImg.png'
imagem = Image.open('./media/img/cruze-sport6-rs-carros.jpg')
logo = Image.open(logo_url)

nova_imagem = imagem.resize((1280, 720))

cords = ((nova_imagem.width - logo.width), (nova_imagem.height - logo.height))
nova_imagem.paste(logo, cords)

nova_imagem.save('./media/img/teste.jpg')



'''requisicao = requests.get(f'http://api.fipeapi.com.br/v1/carros/')
print(requisicao.json()) args slices'''