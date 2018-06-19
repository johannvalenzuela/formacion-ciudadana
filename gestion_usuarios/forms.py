from django import forms
from autenticacion.models import Usuario




class ProfileForm(forms.ModelForm):
    '''
    Formulario editar el profile del usuario
    '''
    nombre = forms.CharField()
    apellido_paterno = forms.CharField()
    apellido_materno = forms.CharField()
    email = forms.EmailField()
    rut = forms.CharField()
    num_documento = forms.CharField()
    fecha_nacimiento = forms.DateField()
    foto = forms.ImageField()


    class Meta:
        model = Usuario
        fields=('nombre','apellido_paterno','apellido_materno','email','rut', 'num_documento', 'fecha_nacimiento', 'foto')