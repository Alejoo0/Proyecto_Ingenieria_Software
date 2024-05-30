from django.contrib import admin
from .models import UsuarioDetalles
from django.contrib.auth import get_user_model
# Register your models here.

class UsuarioDetallesAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nivel_educacional')

User = get_user_model()

admin.site.register(UsuarioDetalles, UsuarioDetallesAdmin)