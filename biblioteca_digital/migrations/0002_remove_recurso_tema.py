# Generated by Django 2.0.4 on 2018-06-03 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_digital', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurso',
            name='tema',
        ),
    ]
