from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    is_admin = models.BooleanField(default=False)

class CategoriaMaterial(models.TextChoices):
    DIDATICO = 'Didático'
    ESCRITORIO = 'Escritório'
    LIMPEZA = 'Limpeza'

class TipoMaterial(models.TextChoices):
    PEDAGOGICO = 'Pedagógico'
    MANUTENCAO = 'Manutenção'
    CONSUMO = 'Consumo'
    OUTROS = 'Outros'

class Material(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CategoriaMaterial.choices)
    quantidade = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return self.nome

class Requisicao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('Pendente', 'Pendente'), ('Aprovado', 'Aprovado'), ('Negado', 'Negado')],
        default='Pendente'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Requisição de {self.usuario.username} para {self.material.nome}'
