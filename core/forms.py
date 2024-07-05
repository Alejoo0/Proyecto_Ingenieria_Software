import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import *

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(label='Nombre', max_length=20)
    apellidos = forms.CharField(label='Apellidos', max_length=30)
    rut = forms.CharField(label='Rut', max_length=15)
    nivel_educacional = forms.ChoiceField(label='Nivel Educativo', choices=NIVELES_CHOICES)
    es_estudiante = forms.BooleanField(label='Es Estudiante', required=False)
    es_profesor = forms.BooleanField(label='Es Profesor', required=False)

    class Meta:
        model = User
        fields = ['nombre', 'apellidos', 'email', 'username', 'rut', 'nivel_educacional', 'password1', 'password2', 'es_estudiante', 'es_profesor']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        
        return email
    
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
            nivel_educacional=self.cleaned_data['nivel_educacional'],
            es_estudiante=self.cleaned_data['es_estudiante'],
            es_profesor=self.cleaned_data['es_profesor']
        )
        return user

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Escribe tu mensaje aquí...',
                'class': 'form-control rounded-pill w-100',
                'style': 'resize: none;'
            }),
        }
        labels = {
            'contenido': ''
        }

class NuevaConversacionForm(forms.Form):
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Seleccione un destinatario",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual')
        super(NuevaConversacionForm, self).__init__(*args, **kwargs)
        
        if usuario_actual.usuariodetalles.es_estudiante:
            # Filtrar solo los profesores
            self.fields['destinatario'].queryset = User.objects.filter(usuariodetalles__es_profesor=True)
        elif usuario_actual.usuariodetalles.es_profesor:
            # Filtrar solo los estudiantes
            self.fields['destinatario'].queryset = User.objects.filter(usuariodetalles__es_estudiante=True)
        else:
            # En caso de otro tipo de usuario, mostrar todos
            self.fields['destinatario'].queryset = User.objects.exclude(id=usuario_actual.id)
