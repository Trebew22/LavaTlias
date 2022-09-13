from django.contrib import admin
from .models import Cliente, Veiculos, Pedido

admin.site.register(Cliente)
admin.site.register(Veiculos)
admin.site.register(Pedido)