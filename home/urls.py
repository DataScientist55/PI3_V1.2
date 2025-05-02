from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('cadastrar/', views.cadastrar_material, name='cadastrar_material'),
    path('listar/', views.listar_materiais, name='listar_materiais'),
    path('controle/', views.controle_pedidos, name='controle_pedidos'),
    path('requisitar/', views.fazer_requisicao, name='fazer_requisicao'),
    path('acompanhar/', views.acompanhar_requisicoes, name='acompanhar_requisicoes'),
    path('login/', views.login_view, name='login'),
    path('materiais/', views.MateriaisListView.as_view(), name='api_materiais'),
    path('requisicoes/', views.RequisicoesListView.as_view(), name='api_requisicoes'),
    path('materiais/<int:pk>/editar/', views.editar_material, name='editar_material'),
    path('materiais/<int:pk>/deletar/', views.excluir_material, name='excluir_material'),
    path('requisicoes/<int:pk>/aprovar/', views.aprovar_requisicao, name='aprovar_requisicao'),
    path('requisicoes/<int:pk>/negar/', views.negar_requisicao, name='negar_requisicao'), 
    path('historico/', views.historico_requisicoes, name='historico_requisicoes'),
    path('gerenciar/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('gerenciar/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('gerenciar/<int:pk>/deletar/', views.excluir_usuario, name='excluir_usuario'),
    path('gerenciar/listar/', views.listar_usuarios, name='listar_usuarios'),
]
