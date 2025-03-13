from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario, Presenca
from .reconhecimento import reconhecer_usuario
from .forms import UsuarioForm

def validar_presenca(request):
    if request.method == 'POST' and request.FILES['foto']:
        imagem = request.FILES['foto']
        usuarios = Usuario.objects.all()

        usuario_encontrado = reconhecer_usuario(imagem, usuarios)
        if usuario_encontrado:
            Presenca.objects.create(usuario=usuario_encontrado)
            return render(request, 'confirmacao.html', {'usuario': usuario_encontrado})
        
        return render(request, 'erro.html', {'mensagem': 'Usuário não reconhecido.'})
    
    return render(request, 'usuarios/upload.html')


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            return redirect('usuario_cadastrado')  # Redireciona para a página de confirmação
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})

