from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def home(request):
    return render(request, 'core/home.html')

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
def user_home(request):
    try:
        usuario_detalles = request.user.usuariodetalles
        nivel_educacional = usuario_detalles.nivel_educacional
        segundo_valor_nivel = None

        for tupla in NIVELES_CHOICES:
            if tupla[0] == nivel_educacional:
                segundo_valor_nivel = tupla[1]
                break
    except UsuarioDetalles.DoesNotExist:
        segundo_valor_nivel = "Funcionario"
    
    return render(request, 'core/home.html', {'nivel_educacional': segundo_valor_nivel})

@login_required
def bandeja_entrada(request):
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user)
    return render(request, 'core/bandeja_entrada.html', {'mensajes': mensajes_recibidos})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST, user=request.user)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            return redirect('mensajes')
    else:
        form = MensajeForm(user=request.user)
    return render(request, 'core/enviar_mensaje.html', {'form': form})
