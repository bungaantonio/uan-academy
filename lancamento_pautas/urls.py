from django.urls import path
from . import views

urlpatterns = [

    path('redirecionar_login/', views.redirecionar_login, name='redirecionar'),

    # Home
    path('quantidade_professores_sessao_ativa/', views.quantidade_professores_sessao_ativa, name='quantidade_professores_sessao_ativa'),
    path('quantidade_estudantes_sessao_ativa/', views.quantidade_estudantes_sessao_ativa, name='quantidade_estudantes_sessao_ativa'),
    
    # Professor
    path('professor/', views.professor_home, name="professor"),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/get_estudantes/', views.get_estudantes, name="get_estudantes"),
    path('atualizar_nota/', views.atualizar_nota, name="atualizar_nota"),
    path('pautas/', views.pautas_estudante, name="pautas_estudante"),
    path('dados_notas_professor/', views.dados_notas_professor, name='dados_notas_professor'),


    # Estudante
    path('estudante/', views.estudante_home, name='estudante'),
    path('estudante/dashboard/', views.estudante_dashboard, name='estudante_dashboard'),
    path('estudante/gerar_pdf', views.gerar_pdf, name='gerar_pdf'),
    path('dados_notas_estudante/', views.dados_notas_estudante, name='dados_notas_estudante'),


    # Administrador
    path('administrador/', views.administrador_home, name='administrador'),
    path('administrador/add-pauta/', views.adicionar_pauta, name='adicionar_pauta'),
    path('administrador/add-nota/', views.adicionar_nota, name='adicionar_nota'),
    path('administrador/add-disciplina/', views.adicionar_disciplina, name='adicionar_disciplina'),
    path('administrador/dashboard/', views.administrador_dashboard, name='dashboard'),
    path('dados_estatisticas_pautas/', views.dados_estatisticas_pautas, name='dados_estatisticas_pautas'),
    
    

]
