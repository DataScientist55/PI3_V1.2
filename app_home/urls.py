from django.urls import path
from . import views
from .views import register, requisitar_material, listar_requisicoes


urlpatterns = [
    path('', views.app_home, name='app_home'),
    path('requisitar/<int:id>/', requisitar_material, name='requisitar_material'),
    path('register/', register, name='register'),
    path('cadastrar/', views.cadastrar_material, name='cadastrar_material'),
    path('materiais/', views.listar_materiais, name='listar_materiais'), 
    path('minhas-requisicoes/', listar_requisicoes, name='listar_requisicoes'),
 
    
]

