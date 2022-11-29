from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastro_cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('att/', views.att, name='att'),
    path('att_cliente/', views.att_cliente, name='att_cliente'),
    path('att_veiculo/<str:id>', views.att_veiculo, name='att_veiculo'),
    path('excluir_veiculo/<str:id>', views.excluir_veiculo, name='excluir_veiculo'),
    path('cadastro_veiculo/', views.cadastro_veiculo, name='cadastro_veiculo'),
    path('cadastro_pedido/', views.cadastro_pedido, name='cadastro_pedido'),
    path('consultar/', views.consultar, name='consultar'),
    path('consulta_unica/<str:ods>', views.consulta_unica, name='consulta_unica'),
    path('ajustar/', views.ajustar, name='ajustar'),
    path('ajustar_lav/', views.ajustar_lav, name='ajustar_lav'),
    path('gerar_pdf/<str:ods>', views.gerar_pdf, name='gerar_pdf'),
    path('enviar_email/<str:ods>', views.enviar_email, name='enviar_email'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)