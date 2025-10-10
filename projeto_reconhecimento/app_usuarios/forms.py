from django import forms
from .models import Reu

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReuForm(forms.ModelForm):
    class Meta:
        model = Reu
        fields = ['nome', 'cpf', 'telefone', 'num_processo', 'foto', 'endereco', 'data_expiracao']  # Campos que o formulário vai incluir
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Reu.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf
        
        

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
            
            self.fields['password1'].widget.attrs.update({'class': 'form-control'})
            self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        