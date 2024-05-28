from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
        return f"{self.user.first_name} {self.user.last_name}"


User = get_user_model()

class FailedLoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    @classmethod
    def record_attempt(cls, user):
        cls.objects.create(user=user)

    @classmethod
    def get_attempts_count(cls, user, within_last_minutes=5):
        cutoff_time = timezone.now() - timezone.timedelta(minutes=within_last_minutes)
        return cls.objects.filter(user=user, timestamp__gte=cutoff_time).count()