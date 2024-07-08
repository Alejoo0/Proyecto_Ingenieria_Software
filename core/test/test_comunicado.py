import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Profesor, Estudiante, Asignatura, Comunicado

class ProfesorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear un usuario para el profesor
        cls.user = User.objects.create_user(username='profesor', first_name='John', last_name='Doe', password='12345')
        # Crear un profesor
        cls.profesor = Profesor.objects.create(user=cls.user)

    def test_profesor_str(self):
        self.assertEqual(str(self.profesor), f"{self.user.first_name} {self.user.last_name}")

class EstudianteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear un usuario para el estudiante
        cls.user = User.objects.create_user(username='estudiante', first_name='Jane', last_name='Doe', password='12345')
        # Crear un estudiante
        cls.estudiante = Estudiante.objects.create(user=cls.user)

    def test_estudiante_str(self):
        self.assertEqual(str(self.estudiante), f"{self.user.first_name} {self.user.last_name}")

class AsignaturaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear un usuario y un profesor
        cls.profesor_user = User.objects.create_user(username='profesor', first_name='John', last_name='Doe', password='12345')
        cls.profesor = Profesor.objects.create(user=cls.profesor_user)

        # Crear un usuario y un estudiante
        cls.estudiante_user = User.objects.create_user(username='estudiante', first_name='Jane', last_name='Doe', password='12345')
        cls.estudiante = Estudiante.objects.create(user=cls.estudiante_user)

        # Crear una asignatura
        cls.asignatura = Asignatura.objects.create(nombre='Matemáticas', profesor=cls.profesor)
        cls.asignatura.estudiantes.add(cls.estudiante)

    def test_asignatura_str(self):
        self.assertEqual(str(self.asignatura), 'Matemáticas')

class ComunicadoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear un usuario para el autor del comunicado
        cls.user = User.objects.create_user(username='autor', first_name='Author', last_name='User', password='12345')

        # Crear un usuario y un profesor
        cls.profesor_user = User.objects.create_user(username='profesor', first_name='John', last_name='Doe', password='12345')
        cls.profesor = Profesor.objects.create(user=cls.profesor_user)

        # Crear un usuario y un estudiante
        cls.estudiante_user = User.objects.create_user(username='estudiante', first_name='Jane', last_name='Doe', password='12345')
        cls.estudiante = Estudiante.objects.create(user=cls.estudiante_user)

        # Crear una asignatura
        cls.asignatura = Asignatura.objects.create(nombre='Matemáticas', profesor=cls.profesor)
        cls.asignatura.estudiantes.add(cls.estudiante)

        # Crear un comunicado
        cls.comunicado = Comunicado.objects.create(
            titulo='Comunicado Importante',
            detalle='Detalles del comunicado',
            detalle_corto='Detalle corto',
            tipo='I',
            asignatura=cls.asignatura,
            publicado_por=cls.user
        )

    def test_comunicado_str(self):
        self.assertEqual(str(self.comunicado), 'Comunicado Importante')