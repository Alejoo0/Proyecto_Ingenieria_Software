from django.db import models
from django.contrib.auth.models import User

TIPO_CHOICES = [
    ("S", "Suspensión de actividades"),
    ("C", "Suspensión de clase"),
    ("I", "Información"),
]

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profesor: {self.user.first_name} {self.user.last_name}"

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Estudiante: {self.user.first_name} {self.user.last_name}"

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    estudiantes = models.ManyToManyField(Estudiante)

    def __str__(self):
        return self.nombre

class Comunicado(models.Model):
    titulo = models.CharField(max_length=55)
    detalle = models.TextField()
    detalle_corto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True, related_name='comunicados_publicados')

    def __str__(self):
        return self.titulo

class Nota(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.FloatField()

    def __str__(self):
        return f"Nota {self.nota} de {self.estudiante} en {self.asignatura}"

class Archivo(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos/')
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.archivo.name} en {self.asignatura}"