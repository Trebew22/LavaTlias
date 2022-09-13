from django.db import models
from datetime import datetime

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=13)
    flag_ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return self.nome

    def retornar_cpf_censurado(self):
        return self.cpf[0]+'**.***.'+self.cpf[8::]

class Veiculos(models.Model):
    modelo = models.CharField(max_length=30)
    marca = models.CharField(max_length=30)
    ano = models.CharField(max_length=4)
    placa = models.CharField(max_length=8)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    imagem = models.ImageField(upload_to="img")

    def __str__(self):
        return self.modelo

class Pedido(models.Model):
    SERVICOS_ESCOLHA = (('M','Mecanico'),
                        ('L', 'Lavagem'))
    
    servicos = models.CharField(max_length=1, choices=SERVICOS_ESCOLHA)    
    descricao = models.CharField(max_length=255)
    veiculo = models.ForeignKey(Veiculos, on_delete=models.DO_NOTHING)
    data_abertura = models.DateTimeField()
    data_finalizacao = models.DateTimeField(auto_now=False, blank=True, null=True)
    ods = models.CharField(max_length=10)
    preco = models.FloatField(blank=True, null=True)
    imagem_final = models.ImageField(upload_to="img_final", null=True, blank=True)
    flag_ativo = models.BooleanField(default=True)
    combinar_preco = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    def data_inicio(self):
        return self.data_abertura.strftime("%d/%m/%Y %H:%M")

    def data_final(self):
        return self.data_finalizacao.strftime("%d/%m/%Y %H:%M")

    '''def save(self, *args, **kwargs):
        self.data_abertura = datetime.now()
        super(Pedido, self).save(*args, **kwargs)'''


