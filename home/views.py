import logging
import traceback
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomUserCreationForm, MaterialForm, RegistroForm, RequisicaoForm
from .models import Material, Requisicao
from .serializers import MaterialSerializer, RequisicaoSerializer

User = get_user_model()

# API Views

class MateriaisListView(APIView):
    def get(self, request):
        materiais = Material.objects.all()  # Corrigido
        serializer = MaterialSerializer(materiais, many=True)
        return Response(serializer.data)


class RequisicoesListView(APIView):
    def get(self, request):
        requisicoes = Requisicao.objects.all()  # Corrigido
        serializer = RequisicaoSerializer(requisicoes, many=True)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()  # Corrigido
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequisicaoViewSet(viewsets.ModelViewSet):
    queryset = Requisicao.objects.all()  # Corrigido
    serializer_class = RequisicaoSerializer
    permission_classes = [permissions.IsAuthenticated]

def home(request):
    return render(request, "home/home.html")

def sobre(request):
    return render(request, "home/sobre.html")

def contato(request):
    return render(request, "home/contato.html")

def cadastrar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material cadastrado com sucesso!')
            return redirect('listar_materiais')

    else:
        form = MaterialForm()
        context = {
            'form': form,
        }   
    return render(request, "materiais/cadastrar.html", context)

logger = logging.getLogger(__name__)

def listar_materiais(request):
    # lista_de_materias = Material.objects.all()

    # context = {
    #     'materiais': lista_de_materias,
    # }
    # return render(request, "materiais/listar.html", context)

    logger.error("--- Entrando na view listar_materiais ---") # Log de entrada
    lista_de_materias = None # Inicializa para garantir que existe
    context = {} # Inicializa contexto
    try:
        logger.error("Tentando executar Material.objects.all()")
        lista_de_materias = Material.objects.all()
        count = lista_de_materias.count() # Força a contagem para ver se a query básica funciona
        logger.error(f"Consulta Material.objects.all() retornou {count} itens.")

        context = {
            'materiais': lista_de_materias,
        }
        logger.error("Contexto criado. Tentando renderizar o template...")

       
        response = render(request, "materiais/listar.html", context)
        logger.error("--- Renderização concluída com sucesso. Saindo da view. ---")
        return response

    except Exception as e:
        # Se QUALQUER exceção ocorrer dentro do bloco try:
        logger.error(f"!!! EXCEÇÃO CAPTURADA na view listar_materiais !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        # Logar o traceback completo formatado
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")

        # Retornar uma resposta de erro genérica para o usuário
        from django.http import HttpResponseServerError
        return HttpResponseServerError("Ocorreu um erro interno no servidor ao listar materiais.")

def controle_pedidos(request):
    return render(request, "pedidos/controle.html")

def fazer_requisicao(request):
    return render(request, "pedidos/fazer.html")

def acompanhar_requisicoes(request):
    return render(request, "requisicoes/acompanhar.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')  # Redireciona para o dashboard ou onde preferir
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')  # Redireciona de volta para login em caso de erro
    else:
        return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label or field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# 🚀 Dashboard Inteligente
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            
            requisicoes = Requisicao.objects.all()
            materiais = Material.objects.all()
            pendentes = requisicoes.filter(status='Pendente')
            contexto = {
                'painel_admin': True,
                'requisicoes': requisicoes,
                'materiais': materiais,

                'pendentes': pendentes,
            }
        else:
            
            requisicoes_usuario = Requisicao.objects.filter(usuario=request.user) # pylint: disable=no-member
            contexto = {
                'painel_admin': False,
                'requisicoes_usuario': requisicoes_usuario,
            }
        return render(request, 'home/dashboard.html', contexto)
    else:
        return redirect('login')

def fazer_requisicao(request):
    if request.method == 'POST':
        form = RequisicaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('acompanhar_requisicoes')
    else:
        form = RequisicaoForm()
    return render(request, 'requisicoes/fazer_requisicao.html', {'form': form})

