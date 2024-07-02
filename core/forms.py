from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Estudiante, Profesor, User, NIVELES_CHOICES

class EstudianteForm(UserCreationForm):
    nivel_educacional = forms.ChoiceField(choices=NIVELES_CHOICES)
    rut = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nivel_educacional', 'rut']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        estudiante = Estudiante.objects.create(
            user=user,
            nivel_educacional=self.cleaned_data['nivel_educacional'],
            rut=self.cleaned_data['rut']
        )
        return user

class ProfesorForm(UserCreationForm):
    especialidad = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'especialidad']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        profesor = Profesor.objects.create(
            user=user,
            especialidad=self.cleaned_data['especialidad']
        )
        return user
   