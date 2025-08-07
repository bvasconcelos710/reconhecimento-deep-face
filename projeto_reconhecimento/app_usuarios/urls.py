from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('validar-presenca/', views.validar_presenca, name='validar_presenca'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario-cadastrado/', views.usuario_cadastrado, name='usuario_cadastrado'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('presencas/', views.listar_presencas, name='listar_presencas'),

]
