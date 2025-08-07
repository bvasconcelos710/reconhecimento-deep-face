from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'telefone', 'num_processo', 'foto']  # Campos que o formulário vai incluir
