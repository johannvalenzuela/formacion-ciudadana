# Generated by Django 2.0.4 on 2018-06-07 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_auto_20180607_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='grupo',
            field=models.ManyToManyField(to='gestion_usuarios.Grupo'),
        ),
    ]
