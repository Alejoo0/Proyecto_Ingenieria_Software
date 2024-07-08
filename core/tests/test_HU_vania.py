
import pytest
from django.contrib.auth.models import User
from core.models import Mensaje  # Asegúrate de importar tu modelo Mensaje

@pytest.mark.django_db
def test_enviar_mensaje():
    # Crea usuarios de prueba
    remitente = User.objects.create(username='remitente')
    destinatario = User.objects.create(username='destinatario')

    # Envía un mensaje
    contenido = "¡Hola! Esto es un mensaje de prueba."
    mensaje = Mensaje.objects.create(remitente=remitente, destinatario=destinatario, contenido=contenido)

    # Verifica que el mensaje se haya creado correctamente
    assert mensaje.remitente == remitente
    assert mensaje.destinatario == destinatario
    assert mensaje.contenido == contenido