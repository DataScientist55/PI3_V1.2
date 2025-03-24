from django.urls import path
from .views import register

app_name = 'app_accounts'  # Se usar namespace, referencie como 'accounts:register'

urlpatterns = [
    path('register/', register, name='register'),
]
