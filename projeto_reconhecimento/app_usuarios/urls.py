from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('', views.inicio, name='inicio'), 
    path('validar-presenca/', views.validar_presenca, name='validar_presenca'),
    path('confirmar-presenca/<int:usuario_id>/', views.confirmar_presenca, name='confirmar_presenca'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario-cadastrado/', views.usuario_cadastrado, name='usuario_cadastrado'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/deletar/<int:usuario_id>/', views.deletar_usuario, name='deletar_usuario'),
    path('presencas/', views.listar_presencas, name='listar_presencas'),
    path('usuarios/<int:usuario_id>/', views.detalhes_usuario, name='detalhes_usuario'),
    path('declaracao/<int:presenca_id>/', views.gerar_declaracao, name='gerar_declaracao'),

]
