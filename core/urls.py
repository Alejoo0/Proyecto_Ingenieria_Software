from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Por ejemplo, una ruta a la vista home
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('comunicados/', views.comunicados,name='comunicados'),
]