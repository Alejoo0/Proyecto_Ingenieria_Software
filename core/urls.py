from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('home/', views.user_home, name='user_home'),
    path('bandeja_entrada/', views.bandeja_entrada, name='bandeja_entrada'),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
]
