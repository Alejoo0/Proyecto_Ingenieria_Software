from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Por ejemplo, una ruta a la vista home
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil ,name='perfil'),
]