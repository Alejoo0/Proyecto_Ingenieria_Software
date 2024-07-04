from django.contrib import admin
from .models import UsuarioDetalles, Profesor, Estudiante, Asignatura, Comunicado, Nota, Archivo
from django.http import HttpResponseForbidden

# Register your models here.

class UsuarioDetallesAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nivel_educacional')

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('user',)

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('user',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(asignatura__profesor__user=request.user)

class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor')
    filter_horizontal = ('estudiantes',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(profesor__user=request.user)

class ComunicadoAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False  # No permitir eliminaciones
    list_display = ("titulo", "tipo", "asignatura", "fecha_publicacion", "publicado_por")
    list_filter = ("fecha_publicacion",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publicado_por=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['asignatura'].queryset = Asignatura.objects.filter(profesor__user=request.user)
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if change and (obj.asignatura.profesor == request.user.profesor or obj.publicado_por != request.user):
                return HttpResponseForbidden("No tienes permiso para editar este comunicado.")
            elif not change:
                obj.publicado_por = request.user
            else:
                obj.modificado_por = request.user
        else:
            if not change:
                obj.publicado_por = request.user
            else:
                obj.modificado_por = request.user
        super().save_model(request, obj, form, change)




admin.site.register(UsuarioDetalles)

admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(Comunicado, ComunicadoAdmin)
admin.site.register(Nota)
admin.site.register(Archivo)