from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django import forms

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

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            form.add_error('email', forms.ValidationError("Este correo electrónico no está registrado."))
            return self.form_invalid(form)
        return super().form_valid(form)