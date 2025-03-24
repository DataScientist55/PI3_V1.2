from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from app_home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls')),  # Inclua as URLs do app home ou app_home aqui
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('app_accounts.urls')),
    path('app_home/', views.app_home, name='app_home'),    

]
