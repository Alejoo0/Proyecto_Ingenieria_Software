from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import UsuarioDetalles
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

@login_required
def pregunta(request):
    user = request.user
    try:
        usuario_detalles = UsuarioDetalles.objects.get(user=user)
        pregunta_display = usuario_detalles.get_pregunta_display()

        if request.method == 'POST':
            respuesta_usuario = request.POST.get('respuesta')
            if respuesta_usuario == usuario_detalles.respuesta:
                # Reiniciar el contador de intentos fallidos en la sesión
                request.session['intentos_fallidos'] = 0
                return redirect('home')
            else:
                # Incrementar el contador de intentos fallidos en la sesión
                intentos_fallidos = request.session.get('intentos_fallidos', 0) + 1
                request.session['intentos_fallidos'] = intentos_fallidos

                if intentos_fallidos >= 3:
                    logout(request)
                    return redirect('bloqueo')  # Redirigir a la página de bloqueo

                error_message = "Respuesta incorrecta. Inténtalo de nuevo."
                return render(request, 'registration/pregunta.html', {
                    'usuario_detalles': usuario_detalles,
                    'pregunta_display': pregunta_display,
                    'error_message': error_message
                })

        return render(request, 'registration/pregunta.html', {
            'usuario_detalles': usuario_detalles,
            'pregunta_display': pregunta_display
        })
    except UsuarioDetalles.DoesNotExist:
        return redirect('home')  # O mostrar un mensaje de error

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def bloqueo(request):
    return render(request, 'registration/bloqueo.html')
