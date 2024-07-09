# test_usuarios.py

import pytest
from django.contrib.auth import get_user_model
from core.forms import CustomUserCreationForm

User = get_user_model()

@pytest.mark.django_db
def test_creacion_usuarios():
    # Crea un usuario de profesor
    profesor_data = {
        'nombre': 'Profesor',
        'apellidos': 'Apellido Profesor',
        'email': 'profesor@example.com',
        'username': 'profesor',
        'rut': '12345678-9',
        'nivel_educacional': 'S',
        'password1': 'contraseña123',
        'password2': 'contraseña123',
        'es_estudiante': False,
        'es_profesor': True,
    }
    profesor_form = CustomUserCreationForm(data=profesor_data)
    assert profesor_form.is_valid()
    profesor = profesor_form.save()

    # Verifica que el usuario de profesor se haya creado correctamente
    assert profesor.usuariodetalles.es_profesor
    assert profesor.usuariodetalles.rut == '12345678-9'
