from django import forms
from .models import Consulta, ConsultaRespuesta
from datetime import datetime
from django.forms.widgets import SelectDateWidget

class ConsultaForm(forms.ModelForm):
    '''
    Formulario para la creacion de la consulta
    '''
    titulo = forms.CharField()
    fecha_finalizacion = forms.DateField(widget=SelectDateWidget, initial=datetime.now) 
    fecha_inicio = forms.DateField(widget=SelectDateWidget, initial=datetime.now) 
    descripcion = forms.CharField(widget= forms.Textarea) 

    class Meta:
            model = Consulta
            fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_finalizacion')

