from django.contrib.auth.models import User
from django.db import models

NIVELES_CHOICES = [
    ("B", "Básica"),
    ("M", "Media"),
    ("S", "Superior")
]
PREGUNTA_CHOICES = [
    ("1", "¿Nombre de tu primera mascota?"),
    ("2", "¿Juego favorito?"),
    ("3", "¿Nombre de tu abuel@?"),
    ("4", "¿lugar nacimiento?")
]

class UsuarioDetalles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField(max_length=15)
    nivel_educacional = models.CharField(max_length=1, choices=NIVELES_CHOICES)
    pregunta = models.CharField(max_length=1, choices=PREGUNTA_CHOICES)
    respuesta = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"