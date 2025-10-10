from django.shortcuts import render, redirect, get_object_or_404
from .models import Reu, Presenca
from .reconhecimento import reconhecer_reu
from .forms import  ReuForm
from .forms import UsuarioRegistroForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def registrar_reu(request):
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
        reus = Reu.objects.all()

        reu_encontrado = reconhecer_reu(imagem, reus)
        if reu_encontrado:
            # Mostra tela de validação ANTES de registrar a presença
            return render(request, 'reus/validar_reu.html', {'reu': reu_encontrado})
        
        return render(request, 'reus/nao_reconhecido.html', {'mensagem': 'Usuário não reconhecido.'})
    
    return render(request, 'reus/verificar.html')

@login_required(login_url='login')
def confirmar_presenca(request, reu_id):
    reu = get_object_or_404(Reu, id=reu_id)
    Presenca.objects.create(reu=reu)
    return render(request, 'reus/reu_reconhecido.html', {'reu': reu})

@login_required(login_url='login')
def cadastrar_reu(request):
    if request.method == 'POST':
        form = ReuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            return redirect('reu_cadastrado')  # Redireciona para a página de confirmação
    else:
        form = ReuForm()

    return render(request, 'reus/cadastrar_reu.html', {'form': form})


@login_required(login_url='login')
def reu_cadastrado(request):
    return render(request, 'reus/reu_cadastrado.html')

@login_required(login_url='login')
def listar_reus(request):
    reus_list = Reu.objects.all()
    paginator = Paginator(reus_list, 10)  # 10 usuários por página
    page_number = request.GET.get('page')
    reus = paginator.get_page(page_number)
    return render(request, 'reus/listar_reus.html', {'reus': reus})

@login_required(login_url='login')
def editar_reu(request, reu_id):
    reu = get_object_or_404(Reu, id=reu_id)

    if request.method == "POST":
        form = ReuForm(request.POST, request.FILES, instance=reu)

        # Verifica se veio uma nova foto da webcam
        nova_foto_base64 = request.POST.get("nova_foto")
        if nova_foto_base64:
            import base64
            from django.core.files.base import ContentFile
            format, imgstr = nova_foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            reu.foto.save(
                f"reu_{reu.id}.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )

        if form.is_valid():
            form.save()
            return redirect('listar_reus')

    else:
        form = ReuForm(instance=reu)

    return render(request, 'reus/editar_reu.html', {
        'form': form,
        'reu': reu  
    })

@login_required(login_url='login')
def deletar_reu(request, reu_id):
    reu = get_object_or_404(Reu, id=reu_id)
    if request.method == "POST":
        reu.delete()
        return redirect('listar_reus')
    return render(request, 'reus/deletar_reu.html', {'reu': reu})

@login_required(login_url='login')
def listar_presencas(request):
    presencas_list = Presenca.objects.select_related('reu').order_by('-data_presenca')
    paginator = Paginator(presencas_list, 10)  # 10 por página

    page_number = request.GET.get('page')
    presencas = paginator.get_page(page_number)

    return render(request, 'reus/listar_presencas.html', {'presencas': presencas})

@login_required(login_url='login')
def detalhes_reu(request, reu_id):
    reu = get_object_or_404(Reu, id=reu_id)

    # Filtra somente as presenças do usuário
    presencas_list = Presenca.objects.filter(reu=reu).order_by('-data_presenca')

    # Aplica paginação (10 registros por página)
    paginator = Paginator(presencas_list, 10)
    page_number = request.GET.get('page')
    presencas = paginator.get_page(page_number)

    return render(
        request,
        'reus/detalhes_reu.html',
        {
            'reu': reu,
            'presencas': presencas
        }
    )
    
def gerar_declaracao(request, presenca_id):
    presenca = get_object_or_404(Presenca, id=presenca_id)

    # Configuração do PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="declaracao_{presenca.reu.nome}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(largura / 2, altura - 80, "DECLARAÇÃO DE PRESENÇA")

    # Corpo do texto
    p.setFont("Helvetica", 12)
    texto = f"""
    Declaramos para os devidos fins que {presenca.reu.nome},
    portador do CPF {presenca.reu.cpf}, compareceu a este fórum de justiça
    no dia {presenca.data_presenca.strftime('%d/%m/%Y')} às {presenca.data_presenca.strftime('%H:%M')}.
    """

    # Quebra de linhas
    y = altura - 150
    for linha in texto.split("\n"):
        p.drawString(80, y, linha.strip())
        y -= 20

    # Rodapé
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(largura / 2, 80, f"Emitido em {datetime.date.today().strftime('%d/%m/%Y')} através do sistema JusFacial")

    p.showPage()
    p.save()

    return response