from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Material, Requisicao

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "is_admin", "is_staff", "is_active")  # Exibe esses campos na lista
    list_filter = ("is_admin", "is_staff", "is_active")  # Adiciona filtros
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissões", {"fields": ("is_admin", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        ("Permissões", {"fields": ("is_admin", "is_staff", "is_active")}),
    )
    search_fields = ("username",)
    ordering = ("username",)

admin.site.register(User, CustomUserAdmin)

class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "quantidade")
    search_fields = ("nome", "categoria")
    list_filter = ("categoria",)

admin.site.register(Material, MaterialAdmin)

class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'material', 'quantidade', 'status', 'data_requisicao')  # Certifique-se de incluir 'data_requisicao'
    list_filter = ('status', 'data_requisicao')  # Adicionando filtro baseado na data de requisição

admin.site.register(Requisicao, RequisicaoAdmin)

