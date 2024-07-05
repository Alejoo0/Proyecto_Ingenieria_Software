from django.contrib import admin
from .models        import Curso, Profesor, Estudiante
# Register your models here.

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_instructor')

    def get_instructor(self, obj):
        return obj.instructor.user.username
    get_instructor.short_description = 'Instructor'

admin.site.register(Curso, CursoAdmin)
admin.site.register(Profesor)
admin.site.register(Estudiante)