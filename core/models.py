from django.contrib.auth.models import User
from django.db import models

NIVELES_CHOICES = [
    ("B", "Básica"),
    ("M", "Media"),
    ("S", "Superior")
]

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    instructor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nivel_educacional = models.CharField(max_length=1, choices=NIVELES_CHOICES)
    rut = models.CharField(max_length=12)
    cursos_inscritos = models.ManyToManyField(Curso, blank=True)

    def __str__(self):
        return self.user.username