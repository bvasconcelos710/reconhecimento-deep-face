from django import forms
from .models import Usuario

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'telefone', 'num_processo', 'foto']  # Campos que o formulário vai incluir
        
        

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Campos de senha vêm do UserCreationForm, então adicionamos aqui:
            self.fields['password1'].widget.attrs.update({'class': 'form-control'})
            self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        