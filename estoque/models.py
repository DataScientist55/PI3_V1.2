from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # Define se o usuário é administrador
    class Meta:
        swappable = 'AUTH_USER_MODEL'  # Permite substituir o modelo de usuário padrão do Django
class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
class Material(models.Model):
    CATEGORIAS = [
        ('Didático', 'Didático'),
        ('Escritório', 'Escritório'),
        ('Limpeza', 'Limpeza'),
    ]
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.quantidade} disponíveis)"
# Modelo de Requisição - Para rastrear pedidos de materiais
class Requisicao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='requisicoes_estoque'  # Nome único para evitar conflito        
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=
                              [('pendente', 'Pendente'), 
                               ('aprovado', 'Aprovado'), 
                               ('negado', 'Negado')], 
                               default='pendente')
    data_requisicao = models.DateTimeField(auto_now_add=True)




