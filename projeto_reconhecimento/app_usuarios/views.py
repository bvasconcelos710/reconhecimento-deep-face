from django.shortcuts import render, redirect
from .models import Usuario, Presenca
from .reconhecimento import reconhecer_usuario
from .forms import UsuarioForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import UsuarioRegistroForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'registration/registrar.html', {'form': form})

@login_required(login_url='login')
def inicio(request):
    return render(request, 'inicio.html')


@login_required(login_url='login')
def validar_presenca(request):
    if request.method == 'POST' and request.FILES['foto']:
        imagem = request.FILES['foto']
        usuarios = Usuario.objects.all()

        usuario_encontrado = reconhecer_usuario(imagem, usuarios)
        if usuario_encontrado:
            Presenca.objects.create(usuario=usuario_encontrado)
            return render(request, 'usuarios/usuario_reconhecido.html', {'usuario': usuario_encontrado})
        
        return render(request, 'usuarios/nao_reconhecido.html', {'mensagem': 'Usuário não reconhecido.'})
    
    return render(request, 'usuarios/verificar.html')


@login_required(login_url='login')
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            return redirect('usuario_cadastrado')  # Redireciona para a página de confirmação
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})


@login_required(login_url='login')
def usuario_cadastrado(request):
    return render(request, 'usuarios/usuario_cadastrado.html')

@login_required(login_url='login')
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required(login_url='login')
def listar_presencas(request):
    presencas_list = Presenca.objects.select_related('usuario').order_by('-data_presenca')
    paginator = Paginator(presencas_list, 10)  # 10 por página

    page_number = request.GET.get('page')
    presencas = paginator.get_page(page_number)

    return render(request, 'usuarios/listar_presencas.html', {'presencas': presencas})