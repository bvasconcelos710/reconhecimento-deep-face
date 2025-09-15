from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Presenca
from .reconhecimento import reconhecer_usuario
from .forms import UsuarioForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import UsuarioRegistroForm
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
    if request.method == 'POST' and request.FILES.get('foto'):
        imagem = request.FILES['foto']
        usuarios = Usuario.objects.all()

        usuario_encontrado = reconhecer_usuario(imagem, usuarios)
        if usuario_encontrado:
            # Mostra tela de validação ANTES de registrar a presença
            return render(request, 'usuarios/validar_usuario.html', {'usuario': usuario_encontrado})
        
        return render(request, 'usuarios/nao_reconhecido.html', {'mensagem': 'Usuário não reconhecido.'})
    
    return render(request, 'usuarios/verificar.html')

@login_required(login_url='login')
def confirmar_presenca(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    Presenca.objects.create(usuario=usuario)
    return render(request, 'usuarios/usuario_reconhecido.html', {'usuario': usuario})

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
    usuarios_list = Usuario.objects.all()
    paginator = Paginator(usuarios_list, 10)  # 10 usuários por página
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required(login_url='login')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)

        # Verifica se veio uma nova foto da webcam
        nova_foto_base64 = request.POST.get("nova_foto")
        if nova_foto_base64:
            import base64
            from django.core.files.base import ContentFile
            format, imgstr = nova_foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            usuario.foto.save(
                f"usuario_{usuario.id}.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')

    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {
        'form': form,
        'usuario': usuario  # 🔑 Aqui está o que faltava!
    })

@login_required(login_url='login')
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/deletar_usuario.html', {'usuario': usuario})

@login_required(login_url='login')
def listar_presencas(request):
    presencas_list = Presenca.objects.select_related('usuario').order_by('-data_presenca')
    paginator = Paginator(presencas_list, 10)  # 10 por página

    page_number = request.GET.get('page')
    presencas = paginator.get_page(page_number)

    return render(request, 'usuarios/listar_presencas.html', {'presencas': presencas})

@login_required(login_url='login')
def detalhes_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Filtra somente as presenças do usuário
    presencas_list = Presenca.objects.filter(usuario=usuario).order_by('-data_presenca')

    # Aplica paginação (10 registros por página)
    paginator = Paginator(presencas_list, 10)
    page_number = request.GET.get('page')
    presencas = paginator.get_page(page_number)

    return render(
        request,
        'usuarios/detalhes_usuario.html',
        {
            'usuario': usuario,
            'presencas': presencas
        }
    )
    
def gerar_declaracao(request, presenca_id):
    presenca = get_object_or_404(Presenca, id=presenca_id)

    # Configuração do PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="declaracao_{presenca.usuario.nome}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(largura / 2, altura - 80, "DECLARAÇÃO DE PRESENÇA")

    # Corpo do texto
    p.setFont("Helvetica", 12)
    texto = f"""
    Declaramos para os devidos fins que {presenca.usuario.nome},
    portador do CPF {presenca.usuario.cpf}, compareceu a este fórum de justiça
    no dia {presenca.data_presenca.strftime('%d/%m/%Y')} às {presenca.data_presenca.strftime('%H:%M')}.
    """

    # Quebra de linhas
    y = altura - 150
    for linha in texto.split("\n"):
        p.drawString(80, y, linha.strip())
        y -= 20

    # Rodapé
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(largura / 2, 80, f"Emitido em {datetime.date.today().strftime('%d/%m/%Y')}")

    p.showPage()
    p.save()

    return response