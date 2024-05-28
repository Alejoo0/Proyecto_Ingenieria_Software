from django.contrib import admin
from .models import UsuarioDetalles
# Register your models here.

class UsuarioDetallesAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nivel_educacional')

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(UsuarioDetalles, UsuarioDetallesAdmin)