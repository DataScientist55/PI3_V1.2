from django.contrib import admin
from django.utils.dateparse import parse_datetime
from .models import Requisicao

@admin.register(Requisicao)
class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_requisicao', 'material','quantidade')
    readonly_fields = ('data_requisicao',)   
    

    
