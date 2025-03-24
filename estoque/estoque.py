from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelos de Usuário
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

# Modelos de Materiais
class CategoriaMaterial(models.TextChoices):
    DIDATICO = "Didático"
    ESCRITORIO = "Escritório"
    LIMPEZA = "Limpeza"

class Material(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CategoriaMaterial.choices)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} ({self.categoria})"

class Requisicao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[("Pendente", "Pendente"), ("Aprovado", "Aprovado"), ("Negado", "Negado")], default="Pendente")
    data_requisicao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.material.nome} ({self.status})"

# Serializers
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_admin"]

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"

class RequisicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisicao
        fields = "__all__"

# Views
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def requisitar(self, request, pk=None):
        material = get_object_or_404(Material, pk=pk)
        quantidade = request.data.get("quantidade", 0)
        if material.quantidade >= int(quantidade):
            requisicao = Requisicao.objects.create(usuario=request.user, material=material, quantidade=quantidade)
            return Response({"status": "Requisição feita", "requisicao_id": requisicao.id})
        return Response({"status": "Quantidade indisponível"}, status=400)

class RequisicaoViewSet(viewsets.ModelViewSet):
    queryset = Requisicao.objects.all()
    serializer_class = RequisicaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def aprovar(self, request, pk=None):
        requisicao = get_object_or_404(Requisicao, pk=pk)
        if requisicao.material.quantidade >= requisicao.quantidade:
            requisicao.material.quantidade -= requisicao.quantidade
            requisicao.material.save()
            requisicao.status = "Aprovado"
            requisicao.save()
            return Response({"status": "Requisição aprovada"})
        return Response({"status": "Quantidade insuficiente"}, status=400)

# Rotas
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'materiais', MaterialViewSet)
router.register(r'requisicoes', RequisicaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
