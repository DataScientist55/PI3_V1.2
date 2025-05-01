import logging
import traceback
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomUserCreationForm, MaterialForm,  RequisicaoForm
from .models import Material, Requisicao
from .serializers import MaterialSerializer, RequisicaoSerializer
from home import models
from django.contrib.auth.decorators import login_required

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


@login_required
def acompanhar_requisicoes(request):

    if request.method == 'POST':
        requisicao_id = request.POST.get('requisicao_id')
        status = request.POST.get('status')

        try:
            requisicao = Requisicao.objects.get(id=requisicao_id)
            requisicao.status = status
            requisicao.save()
            messages.success(request, 'Status atualizado com sucesso!')
        except Requisicao.DoesNotExist:
            messages.error(request, 'Requisição não encontrada.')
    else:
        requisicoes = Requisicao.objects.filter(usuario=request.user)
        return render(request, "requisicoes/acompanhar.html", {'requisicoes': requisicoes})

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


@login_required
def fazer_requisicao(request):
    if request.method == 'POST':
        form = RequisicaoForm(request.POST)
        if form.is_valid():
            try: 
                requisicao = form.save(commit=False)

                requisicao.usuario = request.user  # Atribui o usuário autenticado
                requisicao.save()
                messages.success(request, 'Requisição realizada com sucesso!')
                return redirect('acompanhar_requisicoes')
            except Exception as e:
                logger.error(f"Erro ao salvar a requisição: {e}\n{traceback.format_exc()}")
                messages.error(request, 'Ocorreu um erro ao realizar a requisição.')

                context = {'form': form}

                return render(request, 'requisicoes/fazer_requisicao.html', context)
        else:
            messages.error(request, 'Erro ao validar o formulário. Verifique os dados e tente novamente.')

            context = {'form': form}

            return render(request, 'requisicoes/fazer_requisicao.html', context)
    else:
        form = RequisicaoForm()

    context = {
        'form': form
        }

    return  render(request, 'requisicoes/fazer_requisicao.html', context)

def  editar_material(request, pk):
    '''
    Edita um material existente.
    Se o método for POST, tenta salvar as alterações. Se o formulário for válido, redireciona para a lista de materiais.
    Se o método for GET, exibe o formulário com os dados do material existente.
    '''
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if  form.is_valid():
            form.save()
            messages.success(request, f'Material {material.nome} foi atualizado com sucesso!')
            return redirect('listar_materiais')
    
    else:
        form = MaterialForm(instance=material)

        context = {
            'form': form,
            'material': material
        }

    return render(request, 'materiais/editar.html', context)



logger = logging.getLogger(__name__)

# ... (outras views) ...

def excluir_material(request, pk):
    logger.error(f"--- Entrando na view excluir_material para PK: {pk} ---")
    material = None # Inicializa

    if request.method == 'POST':
        logger.error(f"Método POST detectado para exclusão PK: {pk}")
        try:
            logger.error("Tentando buscar material via get_object_or_404 (POST)...")
            material = get_object_or_404(Material, pk=pk)
            logger.error(f"Material '{material.nome}' encontrado para exclusão.")
            nome_material_excluido = material.nome
            material.delete()
            logger.error(f"Material '{nome_material_excluido}' deletado com sucesso.")
            messages.success(request, f'Material "{nome_material_excluido}" excluído com sucesso!')
            return redirect('listar_materiais')
        except models.ProtectedError:
            logger.error(f"ProtectedError ao tentar excluir material PK: {pk} (Nome: {getattr(material, 'nome', 'N/A')})")
            messages.error(request, f'Não é possível excluir o material "{getattr(material, "nome", "ID "+str(pk))}" pois ele está referenciado em outros registros.')
            return redirect('listar_materiais')
        except Material.DoesNotExist:
            # get_object_or_404 já lida com isso, mas para segurança extra no log
            logger.error(f"Material com PK: {pk} não encontrado durante POST.")
            messages.error(request, f'Material com ID {pk} não encontrado para exclusão.')
            return redirect('listar_materiais')
        except Exception as e:
            logger.error(f"!!! EXCEÇÃO CAPTURADA no POST de excluir_material PK: {pk} !!!")
            logger.error(f"Tipo de Erro: {type(e).__name__}")
            logger.error(f"Mensagem de Erro: {e}")
            logger.error(f"Traceback Completo:\n{traceback.format_exc()}")
            messages.error(request, f'Ocorreu um erro inesperado ao tentar excluir o material.')
            return redirect('listar_materiais') # Ou renderizar uma página de erro

    else: # request.method == 'GET'
        logger.error(f"Método GET detectado para exclusão PK: {pk}")
        try:
            logger.error("Tentando buscar material via get_object_or_404 (GET)...")
            material = get_object_or_404(Material, pk=pk)
            logger.error(f"Material '{material.nome}' encontrado para confirmação.")
            context = {
                'material': material
            }
            logger.error("Contexto criado. Tentando renderizar confirmar_exclusao.html...")
            response = render(request, 'materiais/confirmar_exclusao.html', context)
            logger.error("--- Renderização de confirmar_exclusao.html concluída com sucesso. ---")
            return response
        except Material.DoesNotExist:
             # get_object_or_404 lida com isso, mas logamos explicitamente
            logger.error(f"Material com PK: {pk} não encontrado durante GET para confirmação.")
            # O get_object_or_404 já deve ter retornado 404 aqui, mas se não:
            from django.http import Http404
            raise Http404(f"Material com ID {pk} não encontrado.")
        except Exception as e:
            logger.error(f"!!! EXCEÇÃO CAPTURADA no GET de excluir_material PK: {pk} !!!")
            logger.error(f"Tipo de Erro: {type(e).__name__}")
            logger.error(f"Mensagem de Erro: {e}")
            logger.error(f"Traceback Completo:\n{traceback.format_exc()}")
            # Retornar erro 500 manual, já que o render pode ter falhado
            return HttpResponseServerError("Ocorreu um erro interno ao preparar a página de confirmação de exclusão.")


