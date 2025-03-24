from django import forms
from django.contrib.auth.forms import UserCreationForm
from estoque.models import User
from .models import Requisicao, Material


class CustomUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False, label="Usuário Administrador")
    class Meta:
        model = User
        fields = ["username", "is_admin", "password1", "password2"]

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'categoria', 'quantidade']

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicao
        fields = ['material', 'quantidade']
        
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.filter(quantidade__gt=0)


        
