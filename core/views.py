from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import UsuarioDetalles, NIVELES_CHOICES
from django.contrib.auth.decorators import login_required

def home(request):
    return render (request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def home(request):
    try:
        usuario_detalles = request.user.usuariodetalles
        nivel_educacional = usuario_detalles.nivel_educacional
        segundo_valor_nivel = None

        for tupla in NIVELES_CHOICES:
            if tupla[0] == nivel_educacional:
                segundo_valor_nivel = tupla[1]
                break
    except UsuarioDetalles.DoesNotExist:
        segundo_valor_nivel = "No especificado"
    
    return render(request, 'core/home.html', {'nivel_educacional': segundo_valor_nivel})