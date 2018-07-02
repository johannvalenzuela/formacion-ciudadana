from django import forms
from .models import Recurso, ComentarioRecurso
from .validators import file_size,pdf_type

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
    titulo = forms.CharField(max_length=50,help_text='El título puede tener un máximo de 50 caracteres')
    descripcion = forms.CharField(max_length=255, help_text='La descripción puede tener un máximo de 255 caracteres', widget=forms.Textarea)
    tema = forms.ChoiceField(choices=TEMA_ALTERNATIVAS) 
    imagen_descriptiva = forms.ImageField(validators=[file_size])
    archivo = forms.FileField(validators=[file_size,pdf_type])

    class Meta:
        model = Recurso
        fields = ('titulo', 'descripcion','tema','imagen_descriptiva','archivo',)

class ComentarioForm(forms.ModelForm):
    '''
    Formulario para ingresar un comentario
    '''

    class Meta:
        model = ComentarioRecurso
        fields = ('comentario',)



