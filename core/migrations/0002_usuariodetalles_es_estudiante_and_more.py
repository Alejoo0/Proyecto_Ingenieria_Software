# Generated by Django 5.0.6 on 2024-07-02 14:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariodetalles',
            name='es_estudiante',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuariodetalles',
            name='es_profesor',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('instructor', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('estudiantes', models.ManyToManyField(related_name='cursos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]