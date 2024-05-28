from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import FailedLoginAttempt

def home(request):
    return render (request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


User = get_user_model()

def has_exceeded_failure_limit(username, failure_limit=3, within_last_minutes=5):
    user = User.objects.filter(username=username).first()
    if user is None:
        return False, None
    
    attempts_count = FailedLoginAttempt.get_attempts_count(user, within_last_minutes)
    if attempts_count >= failure_limit:
        return True, user
    
    return False, user
    

def login_view(request):
    intentos = -1
    cuenta_bloqueada = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            exceeded_limit, user= has_exceeded_failure_limit(username)
            if user.check_password(password) == False:
                FailedLoginAttempt.record_attempt(user=user)
                contador=FailedLoginAttempt.get_attempts_count(User.objects.filter(username=username).first(), 5)
            if exceeded_limit:
                form.add_error(None, 'Tu cuenta fue bloqueada debido a que haz excedido el límite de intentos. Intentalo otra vez en 5 minutos')
                form.add_error(None, 'Cualquier intento antes del termino del temporizador lo reiniciará, intentalo una vez termine')
                exceeded_limit, user= has_exceeded_failure_limit(username)
                cuenta_bloqueada = exceeded_limit
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    FailedLoginAttempt.objects.filter(user=user).delete()
                    login(request, user)
                    return redirect('home')  # Redirige a la página de inicio
                else:
                    form.add_error(None, 'Nombre o contraseña incorrectos')
                    
        intentos = 4 - contador
        print(cuenta_bloqueada)            
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'intentos': intentos, 'cuenta_bloqueada':cuenta_bloqueada})