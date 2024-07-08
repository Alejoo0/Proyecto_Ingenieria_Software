from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('registro/', views.registro, name='registro'),
    path('bandeja_entrada/', views.bandeja_entrada, name='bandeja_entrada'),
    path('enviar_mensaje/<int:usuario_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('crear_conversacion/', views.crear_conversacion, name='crear_conversacion'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
]