from django import forms
from .models import Recurso, ComentarioRecurso


class RecursoForm(forms.ModelForm):
    '''
    Formulario para la creacion del recurso academico a traves de un 
    usuario de formacion
    '''
    descripcion = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Recurso
        fields = ('titulo', 'descripcion','imagen_descriptiva',)


class ComentarioForm(forms.ModelForm):
    '''
    Formulario para el ingreso de comentario de un recurso en especifico
    '''
    comentario = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ComentarioRecurso
        fields = ('comentario',)