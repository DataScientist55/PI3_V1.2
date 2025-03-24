from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Material

def home(request):
    materiais = Material.objects.all()  # Ou algum filtro, conforme necessário
    return render(request, 'app_home.html', {'materiais': materiais})

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Substitua 'home' pela sua URL de página inicial
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


