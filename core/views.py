from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def home(request):
    return render (request, 'core/home.html')

def perfil(request):
    return render (request, 'core/perfil.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.rut = form.cleaned_data.get('rut')
            user.save()
            return redirect('login')  # Redirige a la página de login después de registrar
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})