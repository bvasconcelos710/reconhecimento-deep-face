from django.urls import path
from . import views

urlpatterns = [
    
    path('registrar/', views.registrar_reu, name='registrar'),
    path('', views.inicio, name='inicio'), 
    path('validar-presenca/', views.validar_presenca, name='validar_presenca'),
    path('confirmar-presenca/<int:reu_id>/', views.confirmar_presenca, name='confirmar_presenca'),
    path('cadastrar_reu/', views.cadastrar_reu, name='cadastrar_reu'),
    path('reu-cadastrado/', views.reu_cadastrado, name='reu_cadastrado'),
    path('reus/', views.listar_reus, name='listar_reus'),
    path('reus/editar/<int:reu_id>/', views.editar_reu, name='editar_reu'),
    path('reus/deletar/<int:reu_id>/', views.deletar_reu, name='deletar_reu'),
    path('presencas/', views.listar_presencas, name='listar_presencas'),
    path('reus/<int:reu_id>/', views.detalhes_reu, name='detalhes_reu'),
    path('declaracao/<int:presenca_id>/', views.gerar_declaracao, name='gerar_declaracao'),

]
