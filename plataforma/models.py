from django.db import models
from django.dispatch import receiver

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=13)
    flag_ativo = models.BooleanField(default=True)
    lavagens = models.IntegerField(default=0)
    consertos = models.IntegerField(default=0)
    
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
    imagem = models.ImageField(upload_to="img", null=True, blank=True)
    imagem_original = models.ImageField(upload_to="img_original", null=True, blank=True)

    def __str__(self):
        return self.modelo

class Pedido(models.Model):
    SERVICOS_ESCOLHA = (('M','Mecanico'),
                        ('L', 'Lavagem'))
    
    servicos = models.CharField(max_length=1, choices=SERVICOS_ESCOLHA)    
    descricao = models.CharField(max_length=255)
    veiculo = models.ForeignKey(Veiculos, on_delete=models.SET_NULL, null=True) # TODO: salvar uma string com o nome do veiculo(Usando o signals) caso a FK for apagada
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

class Historico(models.Model):
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