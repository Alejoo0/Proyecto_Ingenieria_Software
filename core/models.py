from django.contrib.auth.models import User
from django.db import models

NIVELES_CHOICES = [
    ("B", "Básica"),
    ("M", "Media"),
    ("S", "Superior")
]

class UsuarioDetalles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField(max_length=15)
    nivel_educacional = models.CharField(max_length=1, choices=NIVELES_CHOICES)

    def __str__(self):
        return self.user.email