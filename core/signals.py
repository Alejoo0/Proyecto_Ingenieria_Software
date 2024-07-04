from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Comunicado

@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    if instance.is_staff:
        content_type = ContentType.objects.get_for_model(Comunicado)
        add_permission = Permission.objects.get(codename='add_comunicado', content_type=content_type)
        change_permission = Permission.objects.get(codename='change_comunicado', content_type=content_type)
        instance.user_permissions.add(add_permission, change_permission)