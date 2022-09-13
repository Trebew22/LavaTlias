from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('adicionar_cliente/', views.adicionar_cliente, name='adicionar_cliente'),
    path('cadastro_veiculo/', views.cadastro_veiculo, name='cadastro_veiculo'),
    path('cadastro_pedido/', views.cadastro_pedido, name='cadastro_pedido'),
    path('consultar/', views.consultar, name='consultar'),
    path('consulta_unica/<str:ods>', views.consulta_unica, name='consulta_unica'),
    path('ajustar/<str:ods>', views.ajustar, name='ajustar'),
    path('ajustar_lav/<str:ods>', views.ajustar_lav, name='ajustar_lav'),
    path('gerar_pdf/<str:ods>', views.gerar_pdf, name='gerar_pdf'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)