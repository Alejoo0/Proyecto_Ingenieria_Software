from django.urls import path
from . import views
from .views import EstudianteAutocomplete

urlpatterns = [
    path('', views.home, name='home'),  # Por ejemplo, una ruta a la vista home
    path('registro/', views.registro, name='registro'),
    path('estudiante-autocomplete/', EstudianteAutocomplete.as_view(), name='estudiante-autocomplete'),
]