import logging
import traceback
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.forms import IntegerField
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
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Case, When, Value, IntegerField

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

def is_admin(user):
    return user.is_authenticated and user.is_admin

def home(request):
    return render(request, "home/home.html")

def sobre(request):
    return render(request, "home/sobre.html")

def contato(request):
    return render(request, "home/contato.html")

@login_required
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

@login_required
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

# ==================================================================> Controle de pedidos  <===

@login_required
@user_passes_test(is_admin, login_url='home')
def controle_pedidos(request):
    logger.error(f"--- Entrando na view controle_pedidos (Admin: {request.user.username}) ---")
    requisicoes_pendentes = None 
    context = {}
    
    try: 
        logger.error("Tentando executar Requisicao.objects.filter(status='Pendente')")
        requisicoes_pendentes = Requisicao.objects.filter(status='Pendente').select_related(
             'usuario', 'material', 'material__tipo'
        ).order_by('criado_em')
        
        count = requisicoes_pendentes.count() # Força a contagem para ver se a query básica funciona
        logger.error(f"Consulta Requisições pendentes retornou {count} itens.")

        context = {
            'requisicoes_pendentes': requisicoes_pendentes,

        }
        logger.error("Contexto criado. Tentando renderizar o template de pedidos...")

        response = render(request, "pedidos/controle.html", context)
        logger.error(" --- Renderização de controle_pedidos concluída com sucesso. ---")
        return response
    
    except Exception as e:
        logger.error(f"!!! EXCEÇÃO CAPTURADA na view controle_pedidos !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")

        return HttpResponseServerError("Ocorreu um erro interno no servidor ao listar as requisições pendentes.")

    
    



@login_required
@user_passes_test(is_admin, login_url='home')
def historico_requisicoes(request):
    logger.error(f"--- Entrando na view historico_requisicoes (Admin: {request.user.username}) ---")
    
    try:
        todas_requisicoes = Requisicao.objects.all().select_related(
              'usuario', 'material', 'material__tipo'
        ).order_by('-criado_em')

        count = todas_requisicoes.count()
        logger.error(f"Consulta todas_requisicoes retornou {count} itens.")

        context = {
            'requisicoes': todas_requisicoes,
        }
        
        logger.error("Context criadoo. Tentando renderizar historico_requisicao.html...")
        Response = render(request, "pedidos/historico_requisicao.html", context)
        logger.error(" --- Renderização de historico_requisicao concluída com sucesso. ---")
        return Response
    
    except Exception as e:
        logger.error(f"!!! EXCEÇÃO CAPTURADA na view historico_requisicoes !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")

        return HttpResponseServerError("Ocorreu um erro interno no servidor ao listar as requisições.")

        


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
        requisicoes = Requisicao.objects.filter(usuario=request.user).annotate(
            status_order=Case(
                When(status='Pendente', then=1),
                When(status='Aprovado', then=2),
                When(status='Negada', then=3),
             output_field=IntegerField(),
            )
        ).select_related(
            'material', 'material__tipo' # Otimiza busca de dados relacionados
        ).order_by('status_order', '-criado_em')
        
        return render(request, "requisicoes/acompanhar.html", {'requisicoes': requisicoes})

    return render(request, "requisicoes/acompanhar.html")

@login_required
@user_passes_test(is_admin, login_url='home')
@transaction.atomic
def aprovar_requisicao(request, pk):
    '''
    Aprova uma requisição de material.
    Se o método for POST, tenta aprovar a requisição.
    Se a quantidade requisitada for menor ou igual à quantidade disponível no estoque, atualiza o estoque e salva a requisição como aprovada.

    '''

    if request.method != 'POST':
        messages.error(request, "Método inválido. Apenas POST é permitido.")
        return redirect('controle_pedidos')
    
    requisicao = get_object_or_404(Requisicao, pk=pk, status='Pendente')
    material_requisitado = requisicao.material
    quantidade_requisitada = requisicao.quantidade  

    logger.error(f"Tentando aprovar requisição {pk} para o material {material_requisitado.nome} com quantidade {quantidade_requisitada}.")

    try:
        '''
        Verifica se a quantidade requisitada é menor ou igual à quantidade disponível no estoque.
        Se sim, atualiza o estoque do material e salva a requisição como aprovada.  
        Se não, exibe uma mensagem de erro informando que o estoque é insuficiente.
        '''
        if material_requisitado.quantidade >= quantidade_requisitada:

            material_requisitado.quantidade -= quantidade_requisitada
            material_requisitado.save()
            logger.error(f"Estoque de {material_requisitado.nome} atualizado para {material_requisitado.quantidade}.")

            requisicao.status = 'Aprovado'
            requisicao.save()
            logger.error(f"Requisição {pk} aprovada com sucesso.")

            messages.success(request, f'Requisição {pk} aprovada com sucesso!')
        else:
            logger.warning(f"Estoque insuficiente para o material {material_requisitado.nome}. para aprovar a requisição {pk}. \
                           Necessaria {quantidade_requisitada}, disponível {material_requisitado.quantidade}.")
            messages.error(f"Estoque insuficiente para o material {material_requisitado.nome}. Estoque disponível: {material_requisitado.quantidade}. \
                           Necessário: {quantidade_requisitada}.")
            
    except Exception as e:
        logger.error(f"!!! EXCEÇÃO CAPTURADA ao aprovar requisição {pk} !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")
        messages.error(request, 'Ocorreu um erro ao aprovar a requisição.')

    return redirect('controle_pedidos')

@login_required
@user_passes_test(is_admin, login_url='home')
def negar_requisicao(request, pk):
    
    if request.method != 'POST':
        messages.error(request, "Método inválido. Apenas POST é permitido.")
        return redirect('controle_pedidos')
    
    requisicao = get_object_or_404(Requisicao, pk=pk, status='Pendente')
    logger.error(f"Tentando negar requisição {pk}.")

    try: 
        requisicao .status = 'Negada'
        requisicao.save()
        messages.success(request, f"Requisição {pk} atualizada para 'Negada'")
        messages.info(request, f"Requisilção ID {pk} ({requisicao.material.nome}) foi negada.")
    except Exception as e:
        logger.error(f"!!! EXCEÇÃO CAPTURADA ao negar requisição {pk} !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")
        messages.error(request, 'Ocorreu um erro ao negar a requisição.')
    
    return redirect('controle_pedidos')




# ==================================================================================================================

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

@login_required
@user_passes_test(is_admin, login_url='home')
def gerenciar_usuarios(request):
    logger.info(f"--- Entrando na view gerenciar_usuarios (Admin: {request.user.username}) ---")
    try:
        
        lista_usuarios = User.objects.exclude(pk=request.user.pk).order_by('username')

        logger.info(f"Consulta retornou {lista_usuarios.count()} usuários.")

        context = {
           
            'users': lista_usuarios,
        }

        logger.info("Contexto criado. Tentando renderizar home/gerenciar_users.html...")
      
        response = render(request, 'registration/gerenciar_users.html', context)
        logger.info("--- Renderização de página de gerenciamento concluída. ---")
        return response

    except Exception as e:
        logger.error(f"!!! EXCEÇÃO CAPTURADA na view gerenciar_usuarios !!!")
        logger.error(f"Tipo de Erro: {type(e).__name__}")
        logger.error(f"Mensagem de Erro: {e}")
        logger.error(f"Traceback Completo:\n{traceback.format_exc()}")
        from django.http import HttpResponseServerError
        return HttpResponseServerError("Ocorreu um erro interno ao carregar a página de gerenciamento de usuários.")
    
@login_required
@user_passes_test(is_admin, login_url='home')
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar_usuarios')
    
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/cadastrar.html', context)

@login_required
@user_passes_test(is_admin, login_url='home')
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.username} atualizado com sucesso!')
            return redirect('listar_usuarios')
    
    else:
        form = CustomUserCreationForm(instance=usuario)

        context = {
            'form': form,
            'usuario': usuario
        }

    return render(request, 'usuarios/editar.html', context)

@login_required
@user_passes_test(is_admin, login_url='home')
def excluir_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuário {usuario.username} excluído com sucesso!')
        return redirect('listar_usuarios')
    
    context = {
        'usuario': usuario
    }

    return render(request, 'usuarios/confirmar_exclusao.html', context)

@login_required
@user_passes_test(is_admin, login_url='home')
def listar_usuarios(request):
    usuarios = User.objects.all()
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'usuarios/listar.html', context)





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
                'historico': historico_finalizadas,
                
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


