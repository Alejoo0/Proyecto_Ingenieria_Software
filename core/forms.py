import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profesor, Estudiante, Nota
from dal import autocomplete

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(label='Nombre', max_length=20)
    apellidos = forms.CharField(label='Apellidos', max_length=30)

    class Meta:
        model = User
        fields = ['nombre','apellidos', 'email', 'username', 'password1', 'password2']

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
        
        tipo_usuario = self.cleaned_data.get('tipo_usuario')

        if tipo_usuario == 'profesor':
            Profesor.objects.create(
                user=user,
            )
        elif tipo_usuario == 'estudiante':
            Estudiante.objects.create(
                user=user,
            )
        
        return user

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['asignatura', 'estudiante', 'nota']
        widgets = {
            'estudiante': autocomplete.ModelSelect2(url='estudiante-autocomplete', forward=['asignatura'])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'asignatura' in self.data:
            try:
                asignatura_id = int(self.data.get('asignatura'))
                self.fields['estudiante'].queryset = Estudiante.objects.filter(asignatura__id=asignatura_id)
            except (ValueError, TypeError):
                self.fields['estudiante'].queryset = Estudiante.objects.none()
        elif self.instance.pk:
            self.fields['estudiante'].queryset = self.instance.asignatura.estudiantes.all()
    