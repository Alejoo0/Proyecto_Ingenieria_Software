import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Comunicado, Asignatura

class ComunicadoListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un usuario para las pruebas
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        # Crear un profesor para la asignatura
        profesor = User.objects.create_user(username='profesor', password='12345')

        # Crear una asignatura para los comunicados
        cls.asignatura = Asignatura.objects.create(nombre='Asignatura 1', profesor=profesor)

        # Crear comunicados de prueba
        Comunicado.objects.create(
            titulo='Test Comunicado 1',
            detalle='Detalle 1',
            detalle_corto='Detalle corto 1',
            tipo='S',
            asignatura=cls.asignatura,
            publicado_por=cls.user
        )
        Comunicado.objects.create(
            titulo='Test Comunicado 2',
            detalle='Detalle 2',
            detalle_corto='Detalle corto 2',
            tipo='C',
            asignatura=cls.asignatura,
            publicado_por=cls.user
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/comunicados/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('comunicado_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('comunicado_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/comunicadosAlmnos.html')

    def test_comunicados_displayed(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('comunicado_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Comunicado 1')
        self.assertContains(response, 'Test Comunicado 2')
