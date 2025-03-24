from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.timezone import now

class Material(models.Model):
    CATEGORIAS = [
        ('Didático', 'Didático'),
        ('Escritório', 'Escritório'),
        ('Limpeza', 'Limpeza'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.quantidade} disponíveis)"

class Requisicao(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    data_requisicao = models.DateTimeField(auto_now_add=True)
    related_name='requisicoes_app_home'

    def __str__(self):
        return f"{self.usuario.username} - {self.material.nome} ({self.quantidade}) - {self.status}"    

    def save(self, *args, **kwargs):
        if isinstance(self.data_requisicao, str):
            self.data_requisicao = datetime.fromisoformat(self.data_requisicao)
        super().save(*args, **kwargs)
    


