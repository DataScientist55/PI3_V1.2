from rest_framework import serializers
from .models import Material, Requisicao, Usuario

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class RequisicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisicao
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'is_admin']
