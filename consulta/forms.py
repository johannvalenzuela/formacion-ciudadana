from django import forms
from .models import Consulta
from datetime import datetime

class consultaForm(forms.ModelForm):
    '''
    Formulario para la creacion de la consulta
    '''
    titulo = forms.CharField()
    fecha_finalizacion = models.DateField(widget=SelectDateWidget, initial=datetime.now) 
    fecha_inicio = models.DateField(widget=SelectDateWidget, initial=datetime.now) 
    descripcion = forms.CharField(widget= froms.Textarea) 

    class Meta:
            model = Consulta
            fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_finalizacion')