from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from .models import Material, Requisicao
from django.contrib.auth.forms import UserCreationForm
from .forms import MaterialForm, RequisicaoForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def app_home(request):
    from .models import Material  # Importação tardia
    materiais = Material.objects.all()
    return render(request, 'app_home.html', {'materiais': materiais})


def requisitar_material(request, id):
    material = get_object_or_404(Material, id=id)
    if request.method == 'POST':
            pass
    return render(request, 'requisitar_material.html', {'material': material})

def aap_home(request):
    materiais = Material.objects.all()
    requisicoes = Requisicao.objects.filter(user=request.user)  # Supondo que a requisição tenha uma relação com o usuário
    return render(request, 'app_home.html', {'materiais': materiais, 'requisicoes': requisicoes})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Substitua 'home' pela sua URL de página inicial
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def cadastrar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_home')  # Redirecionar para a página inicial após cadastro
    else:
        form = MaterialForm()

    return render(request, 'app_home/cadastrar_material.html', {'form': form})

def listar_materiais(request):
    materiais = Material.objects.all()  # Obtém todos os materiais cadastrados
    return render(request, 'app_home/listar_materiais.html', {'materiais': materiais})

def requisitar_material(request):
    if request.method == 'POST':
        form = RequisicaoForm(request.POST)
        if form.is_valid():
            requisicao = form.save(commit=False)
            data_requisicao = form.cleaned_data['data_requisicao']
                       
            if isinstance(data_requisicao, str):
                requisicao.data_requisicao = datetime.fromisoformat(data_requisicao)
            
            requisicao.save()
            return redirect('sucesso')  # Redireciona após o sucesso
    else:
        form = RequisicaoForm()

    return render(request, 'requisitar_material.html', {'form': form})

@login_required
def listar_requisicoes(request):
    requisicoes = Requisicao.objects.filter(usuario=request.user)
    return render(request, 'app_home/listar_requisicoes.html', {'requisicoes': requisicoes})

