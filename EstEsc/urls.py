from django.contrib import admin
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),       
]

def home(request):
    url = reverse('login')
    return HttpResponseRedirect(url)
