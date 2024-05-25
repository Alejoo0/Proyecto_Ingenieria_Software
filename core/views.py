from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UsuarioDetalles
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'core/home.html')

@login_required
def pregunta(request):
    user = request.user
    try:
        usuario_detalles = UsuarioDetalles.objects.get(user=user)
        pregunta_display = usuario_detalles.get_pregunta_display()
        return render(request, 'registration/pregunta.html', {
            'usuario_detalles': usuario_detalles,
            'pregunta_display': pregunta_display
        })
    except UsuarioDetalles.DoesNotExist:
        return redirect('home')  # Or show an error message

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})
