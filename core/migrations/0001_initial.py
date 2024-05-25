# Generated by Django 5.0.6 on 2024-05-25 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioDetalles',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rut', models.CharField(max_length=15)),
                ('nivel_educacional', models.CharField(choices=[('B', 'Básica'), ('M', 'Media'), ('S', 'Superior')], max_length=1)),
            ],
        ),
    ]
