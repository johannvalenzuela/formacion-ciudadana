# Generated by Django 2.0.4 on 2018-06-07 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autenticacion', '0001_initial'),
        ('gestion_usuarios', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='grupo',
            field=models.ManyToManyField(blank=True, null=True, to='gestion_usuarios.Grupo'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
