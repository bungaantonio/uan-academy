from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO

from lancamento_pautas.models import Disciplina, Pauta, Estudante, Nota, Professor
from .decorators import professor_required, estudante_required, administrador_required
from .forms import SubmeterDisciplinaForm, SubmeterNotaForm, SubmeterPautaForm

import logging

logger = logging.getLogger(__name__)


@login_required
def home(request):
    contexto = {
        'is_administrador': request.user.groups.filter(name='Administradores').exists(),
        'is_professor': request.user.groups.filter(name='Professores').exists(),
        'is_estudante': request.user.groups.filter(name='Estudantes').exists(),
    }
    return render(request, 'home.html', contexto)


def quantidade_professores_sessao_ativa(request):
    # Definindo o tempo limite para considerar a sessão ativa (2 minutos)
    tempo_ativo_limite = timezone.now() - timedelta(minutes=2)

    # Filtrar usuários que são professores e têm sessão ativa
    professores_sessao_ativa = User.objects.filter(
        groups__name='Professores', is_active=True, last_login__gte=tempo_ativo_limite)

    # Pegar os usernames dos professores com sessão ativa
    professores_nomes = [
        professor.username for professor in professores_sessao_ativa]

    data = {
        'professores_sessao_ativa': professores_sessao_ativa.count(),
        'professores_nomes': professores_nomes,
    }

    return JsonResponse(data)


def quantidade_estudantes_sessao_ativa(request):
    # Definindo o tempo limite para considerar a sessão ativa (2 minutos)
    tempo_ativo_limite = timezone.now() - timedelta(minutes=2)

    # Filtrar usuários que são estudantes e têm sessão ativa
    estudantes_sessao_ativa = User.objects.filter(
        groups__name='Estudantes', is_active=True, last_login__gte=tempo_ativo_limite)

    # Pegar os usernames dos estudantes com sessão ativa
    estudantes_nomes = [
        estudante.username for estudante in estudantes_sessao_ativa]

    data = {
        'estudantes_sessao_ativa': estudantes_sessao_ativa.count(),
        'estudantes_nomes': estudantes_nomes,
    }

    return JsonResponse(data)


def redirecionar_login(request):
    if request.user.groups.filter(name='Professores').exists():
        return redirect('professor')
    elif request.user.groups.filter(name='Estudantes').exists():
        return redirect('estudante')
    elif request.user.groups.filter(name='Administradores').exists():
        return redirect('administrador')
    else:
        return HttpResponse('Não és um usuário reconhecido pelo nosso software, contactar o pessoal interno...')


@login_required
@professor_required
def professor_home(request):
    try:
        professor = request.user.professor
        disciplinas = Disciplina.objects.filter(professor=professor)
    except Professor.DoesNotExist:
        return HttpResponse('Vamos resolver')
    contexto = {
        'disciplinas': disciplinas,
        'is_professor': True
    }
    return render(
        request,
        'professor/home.html',
        contexto
    )


@login_required
@professor_required
def professor_dashboard(request):
    contexto = {
        'is_professor': True
    }
    return render(request, 'professor/dashboard.html', contexto)


@login_required
@professor_required
def get_estudantes(request):
    disciplina_id = request.GET.get('disciplina')

    if disciplina_id:
        pautas = Pauta.objects.filter(disciplina_id=disciplina_id)
    else:
        pautas = []

    contexto = {
        'pautas': pautas
    }

    return render(request, 'professor/tabela_estudantes.html', contexto)


@login_required
@professor_required
def pautas_estudante(request):
    estudante = get_object_or_404(Estudante, user=request.user)
    pautas = Pauta.objects.filter(estudante=estudante)

    contexto = {
        'pautas': pautas
    }

    return render(request, 'professor/pauta_estudante.html', contexto)


@login_required
@csrf_exempt  # desabilitar csrf
@professor_required
def atualizar_nota(request):
    estudante_id = request.POST.get('estudante_id')

    nota = request.POST.get('nota')
    tipo = request.POST.get('tipo')

    estudante = get_object_or_404(Nota, id=estudante_id)

    if tipo == 'AC1':
        estudante.AC1 = float(nota)
    elif tipo == 'AC2':
        estudante.AC2 = float(nota)
    elif tipo == 'PF1':
        estudante.PF1 = float(nota)
    elif tipo == 'PF2':
        estudante.PF2 = float(nota)

    estudante.save()

    data = {
        'media_semestral': estudante.media_semestral(),
        'resultado_final': estudante.resultado_final()
    }

    return JsonResponse(data)


@login_required
@estudante_required
def estudante_home(request):
    try:
        estudante = request.user.estudante
        nota_disponivel = Nota.objects.filter(estudante=estudante)
    except Estudante.DoesNotExist:
        return HttpResponse('Entre em contacto com o departamento para verificar o seu acesso!')

    contexto = {
        'nota_disponivel': nota_disponivel,
        'is_estudante': True
    }
    return render(request, 'estudante/home.html', contexto)


@estudante_required
def estudante_dashboard(request):
    contexto = {
        'is_estudante': True
    }
    return render(request, 'estudante/dashboard.html', contexto)


@estudante_required
def gerar_pdf(request):
    response = FileResponse(
        gerar_ficheiro_pdf(request),
        as_attachment=True,
        filename='Notas.pdf'
    )
    return response


def gerar_ficheiro_pdf(request):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    estudante = request.user.estudante
    notas = Nota.objects.filter(estudante=estudante)

    # Criando elementos do relatório
    elements = []

    # Estilos para o texto
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_normal = styles['Normal']

    # Adicionando parágrafos de texto
    titulo = "<b>Relatório de Notas</b>"
    paragraph = Paragraph(titulo, estilo_titulo)
    elements.append(paragraph)

    info_estudante = f"Este é um relatório de notas gerado automaticamente para o estudante {
        estudante.user.get_full_name()}."
    paragraph = Paragraph(info_estudante, estilo_normal)
    elements.append(paragraph)

    # Adicionando uma tabela
    data = [['Disciplina', 'AC1', 'AC2', 'PF1', 'PF2', 'Média Semestral']]

    for nota in notas:
        row = [
            nota.pauta.disciplina,
            str(nota.AC1),
            str(nota.AC2),
            str(nota.PF1),
            str(nota.PF2),
            str(nota.media_semestral())
        ]
        data.append(row)

    table = Table(data)
    style = TableStyle([
        # Cor de fundo para o cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        # Cor do texto para o cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # Alinhamento centralizado para todo o conteúdo
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # Alinhamento vertical no centro para todo o conteúdo
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Linhas internas da tabela
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),      # Borda da tabela
    ])
    table.setStyle(style)
    elements.append(table)

    # Construindo o PDF
    pdf.build(elements)
    buffer.seek(0)
    return buffer


# ADMINISTRADOR
@login_required
@administrador_required
def administrador_home(request):
    pautas = Pauta.objects.all()

    contexto = {
        'pautas': pautas,
        'is_administrador': True
    }
    return render(request, 'administrador/home.html', contexto)


@login_required
@administrador_required
def adicionar_pauta(request):
    if request.method == 'POST':
        logger.debug("Formulário submetido. Dados: %s", request.POST)

        form = SubmeterPautaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pauta submetida com sucesso!')
            logger.debug("Pauta submetida com sucesso!")
            return HttpResponseRedirect(reverse('adicionar_pauta'))
        else:
            messages.error(
                request, 'Erro ao submeter a pauta. Verifique o formulário e tente novamente.')
            logger.debug("Erro submetida a pauta!")

    else:
        form = SubmeterPautaForm()

    contexto = {
        'form': form,
        'is_administrador': True
    }
    return render(request, 'administrador/add_pauta.html', contexto)


@login_required
@administrador_required
def adicionar_disciplina(request):
    if request.method == 'POST':
        logger.debug("Formulário submetido. Dados: %s", request.POST)

        form = SubmeterDisciplinaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina submetida com sucesso!')
            logger.debug("Disciplina submetida com sucesso!")
            return HttpResponseRedirect(reverse('adicionar_disciplina'))
        else:
            messages.error(
                request, 'Erro ao submeter a disciplina. Verifique o formulário e tente novamente.')
            logger.debug("Erro submetida a disciplina!")

    else:
        form = SubmeterDisciplinaForm()

    disciplinas = Disciplina.objects.all().order_by('id')

    contexto = {
        'form': form,
        'is_administrador': True,
        'disciplinas': disciplinas
    }
    return render(request, 'administrador/add_disciplina.html', contexto)


@login_required
@administrador_required
def adicionar_nota(request):
    if request.method == 'POST':

        form = SubmeterNotaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Nota submetida com sucesso!')
            return HttpResponseRedirect(reverse('adicionar_nota'))
        else:
            messages.error(
                request, 'Erro ao submeter a nota. Verifique o formulário e tente novamente.')
            logger.debug("Erro submetida a nota!")

    else:
        form = SubmeterNotaForm()

    notas = Nota.objects.all().order_by('estudante__numero')  # ajustar para nome

    contexto = {
        'form': form,
        'is_administrador': True,
        'notas': notas
    }
    return render(request, 'administrador/add_nota.html', contexto)


@login_required
@administrador_required
def administrador_dashboard(request):
    contexto = {
        'is_administrador': True
    }
    return render(request, 'administrador/dashboard.html', contexto)


@login_required
@administrador_required
def dados_estatisticas_pautas(request):
    # Consulta para obter estatísticas de pautas por disciplina, incluindo nomes das disciplinas
    estatisticas = Pauta.objects.values(
        'disciplina__codigo').annotate(quantidade_pautas=Count('id'))
    print(estatisticas)
    disciplinas = []
    quantidade_pautas = []

    for item in estatisticas:
        # Usar 'disciplina__nome' para pegar o nome da disciplina
        disciplinas.append(item['disciplina__codigo'])
        quantidade_pautas.append(item['quantidade_pautas'])

    data = {
        'disciplinas': disciplinas,
        'quantidade_pautas': quantidade_pautas,
    }

    return JsonResponse(data)


@login_required
@estudante_required
def dados_notas_estudante(request):
    estudante = get_object_or_404(Estudante, user=request.user)

    notas = Nota.objects.filter(estudante=estudante)

    data = {
        'disciplinas': [],
        'notas_ac1': [],
        'notas_ac2': [],
        'notas_pf1': [],
        'notas_pf2': [],
        'notas_media_semestral': [],
        'desempenho_satisfatorio': [],
    }

    for nota in notas:
        data['disciplinas'].append(nota.pauta.disciplina.nome)
        data['notas_ac1'].append(nota.AC1)
        data['notas_ac2'].append(nota.AC2)
        data['notas_pf1'].append(nota.PF1)
        data['notas_pf2'].append(nota.PF2)
        data['notas_media_semestral'].append(nota.media_semestral())
        # Lógica para verificar se o desempenho é satisfatório
        desempenho_satisfatorio = nota.media_semestral() >= 7.0
        data['desempenho_satisfatorio'].append(desempenho_satisfatorio)

    return JsonResponse(data)


@login_required
@professor_required
def dados_notas_professor(request):
    # Recupera as disciplinas do professor logado
    disciplinas = Disciplina.objects.filter(professor=request.user.professor)

    data = {
        'disciplinas': [],
        'notas_ac1': [],
        'notas_ac2': [],
        'notas_pf1': [],
        'notas_pf2': [],
        'melhor_estudante': None,
        'media_melhor_estudante': None,
    }

    melhor_media = -1
    melhor_estudante = None

    # Itera sobre as disciplinas para obter as médias das notas e o melhor estudante
    for disciplina in disciplinas:
        # Filtra todas as pautas relacionadas à disciplina
        pautas = Pauta.objects.filter(disciplina=disciplina)

        # Calcula a média das notas para cada tipo de avaliação
        media_ac1 = Nota.objects.filter(pauta__in=pautas).aggregate(Avg('AC1'))[
            'AC1__avg'] or 0
        media_ac2 = Nota.objects.filter(pauta__in=pautas).aggregate(Avg('AC2'))[
            'AC2__avg'] or 0
        media_pf1 = Nota.objects.filter(pauta__in=pautas).aggregate(Avg('PF1'))[
            'PF1__avg'] or 0
        media_pf2 = Nota.objects.filter(pauta__in=pautas).aggregate(Avg('PF2'))[
            'PF2__avg'] or 0

        # Adiciona as médias calculadas aos dados
        data['disciplinas'].append(disciplina.nome)
        data['notas_ac1'].append(media_ac1)
        data['notas_ac2'].append(media_ac2)
        data['notas_pf1'].append(media_pf1)
        data['notas_pf2'].append(media_pf2)

        # Encontra o estudante com a maior média de notas nesta disciplina
        estudante_melhor_media = Nota.objects.filter(pauta__in=pautas).values('estudante').annotate(
            media=(Avg('AC1') + Avg('AC2') + Avg('PF1') + Avg('PF2')) / 4
        ).order_by('-media').first()

        if estudante_melhor_media and estudante_melhor_media['media'] > melhor_media:
            melhor_media = estudante_melhor_media['media']
            melhor_estudante = estudante_melhor_media['estudante']
            data['melhor_estudante'] = melhor_estudante
            data['media_melhor_estudante'] = melhor_media

    # Converte o ID do melhor estudante para o seu nome (alteração aqui)
    if melhor_estudante:
        melhor_estudante_obj = Estudante.objects.get(id=melhor_estudante)
        # Você pode escolher aqui se deseja retornar o nome ou outro atributo do estudante
        # ou .numero ou .outro_atributo
        data['melhor_estudante'] = melhor_estudante_obj.user.username

    return JsonResponse(data)
