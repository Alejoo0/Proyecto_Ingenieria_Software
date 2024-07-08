import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profesor, Curso, Estudiante, NIVELES_CHOICES

class ModelTests(TestCase):

    def setUp(self):
        # Crear un usuario
        self.user_profesor = User.objects.create_user(username='profesor1', password='pass1234')
        self.user_estudiante = User.objects.create_user(username='estudiante1', password='pass1234')

        # Crear un profesor
        self.profesor = Profesor.objects.create(user=self.user_profesor, especialidad='Matemáticas')

        # Crear un curso
        self.curso = Curso.objects.create(
            nombre='Curso de Álgebra',
            instructor=self.profesor,
            descripcion='Un curso avanzado de álgebra'
        )

        # Crear un estudiante
        self.estudiante = Estudiante.objects.create(
            user=self.user_estudiante,
            nivel_educacional='M',
            rut='12345678-9'
        )
        self.estudiante.cursos_inscritos.add(self.curso)

    def test_profesor_str(self):
        self.assertEqual(str(self.profesor), self.user_profesor.username)

    def test_curso_str(self):
        self.assertEqual(str(self.curso), 'Curso de Álgebra')

    def test_estudiante_str(self):
        self.assertEqual(str(self.estudiante), self.user_estudiante.username)

    def test_estudiante_nivel_educacional(self):
        self.assertEqual(self.estudiante.nivel_educacional, 'M')

    def test_estudiante_cursos_inscritos(self):
        self.assertIn(self.curso, self.estudiante.cursos_inscritos.all())