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
]
