from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('rut', 'nombre', 'apellido_paterno','apellido_materno', 'email', 
                    'fecha_nacimiento', 'num_documento')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = UserChangeForm.Meta.fields