import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioDetalles, NIVELES_CHOICES

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(label='Nombre', max_length=20)
    apellidos = forms.CharField(label='Apellidos', max_length=30)
    rut = forms.CharField(label='Rut', max_length=15)
    nivel_educacional = forms.ChoiceField(label='Nivel Educativo', choices=NIVELES_CHOICES)

    class Meta:
        model = User
        fields = ['nombre','apellidos', 'email', 'username', 'rut', 'nivel_educacional', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios = ['gmail.com', 'outlook.com', 'hotmail.com', 'gmail.cl', 'outlook.cl', 'hotmail.cl']
        dominio = email.split('@')[-1]
        if dominio not in dominios :
            raise forms.ValidationError('El correo no cumple con el formato \n Ej: usuario@gmail.cl')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username
    
    def validar_rut(self, rut):
        rut = rut.replace('.', '').upper()
        
        if not re.match(r'^\d{7,8}-[0-9K]$', rut):
            raise forms.ValidationError('El formato del RUT no es válido')

        if UsuarioDetalles.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado')

        return rut

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        rut_validado = self.validar_rut(rut)
        return rut_validado

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellidos']
        user.save()
        UsuarioDetalles.objects.create(
            user=user,
            rut=self.cleaned_data['rut'],
            nivel_educacional=self.cleaned_data['nivel_educacional']
        )
        return user
    