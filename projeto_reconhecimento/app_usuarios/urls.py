from django.urls import path
from . import views

urlpatterns = [
    path('', views.validar_presenca, name='validar_presenca'),
    path('validar-presenca/', views.validar_presenca, name='validar_presenca'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
]
