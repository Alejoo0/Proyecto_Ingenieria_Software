from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def home(request):
    nivel_educacional = get_nivel_educacional(request)
    return render(request, 'core/home.html', {'nivel_educacional': nivel_educacional})

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    nivel_educacional = get_nivel_educacional(request)
    return render(request, 'registration/registro.html', {'form': form, 'nivel_educacional': nivel_educacional})

@login_required
def user_home(request):
    nivel_educacional = get_nivel_educacional(request)
    return render(request, 'core/home.html', {'nivel_educacional': nivel_educacional})

@login_required
def bandeja_entrada(request):
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user)
    nivel_educacional = get_nivel_educacional(request)
    return render(request, 'core/bandeja_entrada.html', {'mensajes': mensajes_recibidos, 'nivel_educacional': nivel_educacional})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST, user=request.user)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect('bandeja_entrada')  # Redirige a la página de mensajes después de enviar el mensaje
    else:
        form = MensajeForm(user=request.user)  # Aquí se define el formulario para el método GET
    
    nivel_educacional = get_nivel_educacional(request)
    return render(request, 'core/enviar_mensaje.html', {'form': form, 'nivel_educacional': nivel_educacional})


def get_nivel_educacional(request):
    if request.user.is_authenticated:
        try:
            usuario_detalles = request.user.usuariodetalles
            nivel_educacional = usuario_detalles.get_nivel_educacional_display()
        except UsuarioDetalles.DoesNotExist:
            nivel_educacional = "No especificado"
    else:
        nivel_educacional = None
    return nivel_educacional
