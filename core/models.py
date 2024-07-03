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
    es_estudiante = models.BooleanField(default=True)
    es_profesor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.remitente.username} a {self.destinatario.username}"
