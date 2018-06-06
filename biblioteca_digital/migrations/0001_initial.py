# Generated by Django 2.0.4 on 2018-06-05 00:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioRecurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('autorComentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.CharField(max_length=255)),
                ('imagen_descriptiva', models.FileField(upload_to='imagenes/')),
                ('fecha_creacion', models.DateTimeField(default=datetime.datetime.now)),
                ('tema', models.PositiveSmallIntegerField(choices=[(1, 'formacion ciudadana'), (2, 'convivencia escolar'), (3, 'otros')], default=1)),
                ('archivo', models.FileField(upload_to='recursos/')),
                ('valoracionTotal', models.FloatField(default=0)),
                ('cant_valoracion', models.PositiveIntegerField(default=0)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ValoracionRecurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valoracion', models.FloatField(default=0)),
                ('recurso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca_digital.Recurso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comentariorecurso',
            name='recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca_digital.Recurso'),
        ),
    ]
