from django import forms
from .models import Recurso, ComentarioRecurso

TEMA_ALTERNATIVAS = (
    (1, 'formacion ciudadana'),
    (2, 'convivencia escolar'),
    (3, 'otros'),
)

class RecursoForm(forms.ModelForm):
    '''
    Formulario para la creacion y modificacion del recurso academico
    a traves de un usuario de formacion
    '''
    titulo = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    tema = forms.ChoiceField(choices=TEMA_ALTERNATIVAS) 
    imagen_descriptiva = forms.ImageField()
    archivo = forms.FileField(widget=forms.FileInput)

    class Meta:
        model = Recurso
        fields = ('titulo', 'descripcion','imagen_descriptiva','tema','archivo',)


class ComentarioForm(forms.ModelForm):
    '''
    Formulario para el ingreso de comentario de un recurso en especifico
    '''
    comentario = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ComentarioRecurso
        fields = ('comentario',)