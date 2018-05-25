from django import forms
from .models import Recurso



class RecursoForm(forms.ModelForm):
'''
Formulario para la creacion del recurso academico a traves de un 
usuario de formacion
'''
    descripcion = forms.CharField(widget=forms.Textarea)

    class Meta:
            model = Recurso
            fields = ('titulo', 'descripcion','imagen_descriptiva',)

