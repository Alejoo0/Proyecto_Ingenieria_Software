from django.contrib import admin
from django.http import HttpResponseForbidden
from .models import Profesor, Estudiante, Asignatura, Comunicado, Nota, Archivo
from .forms import NotaForm

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

class NotaAdmin(admin.ModelAdmin):
    form = NotaForm
    list_display = ('asignatura', 'estudiante', 'nota')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(asignatura__profesor__user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['asignatura'].queryset = Asignatura.objects.filter(profesor=request.user.profesor)
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if obj.asignatura.profesor == request.user.profesor:
                obj.save()
            else:
                return HttpResponseForbidden("No tienes permiso para agregar una nota para esta asignatura.")
        else:
            obj.save()

admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(Comunicado, ComunicadoAdmin)
admin.site.register(Nota, NotaAdmin)
admin.site.register(Archivo)