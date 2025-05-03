from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Requisicao, Material

User = get_user_model()

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']      

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email", "password1", "password2")

class RequisicaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.select_related('tipo')
        self.fields['material'].label_from_instance = lambda obj: f"{obj.nome}{f' - {obj.tipo.nome}' if obj.tipo else ' - Sem Tipo'}"

    class Meta:
        model = Requisicao
        fields = ['material', 'quantidade']


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
      

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_admin']   

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }