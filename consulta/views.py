from django.shortcuts import render
from django.views import generic
from .models import Consulta
from .forms import ConsultaPropuestaForm, ConsultaForm


class VisualizarConsultasView(generic.ListView):
    '''
    Muestra la vista de todas las consultas que el usuario puede ver
    '''
    template_name = 'consulta/visualizar_consultas.html'
    context_object_name = 'lista_consultas'

    def get_queryset(self):
        """Retorna las consultas."""
        return Consulta.objects.all()

class CrearConsultaView(generic.CreateView):
    '''
    Muesta la vista para crear una consulta nueva
    '''
    form_class = ConsultaForm
    template_name = 'consulta/crear_consulta.html'

class ConsultaCrearPropuestaView(generic.CreateView):
    '''
    Muestra la vista para crear una propuesta(respuesta) de una consulta
    '''
    form_class = ConsultaPropuestaForm
    template_name = 'consulta/crear_propuesta_consulta.html'

class ConsultaVisualizarPropuestaView(generic.CreateView):
    '''
    Muestra la vista para ver una propuesta(respuesta) de una consulta
    '''
    form_class = ConsultaPropuestaForm
    template_name = 'consulta/visualizar_propuesta_consulta.html'

class ResultadoConsultaView(generic.DetailView):
    '''
    Muesta la vista del resultado de una consulta en especifico
    '''
    model = Consulta
    template_name = 'consulta/resultado_consulta.html'

class ResponderConsultaView(generic.TemplateView):
    '''
    Muestra la vista para responder una consulta
    '''
    model = Consulta
    template_name = 'consulta/responder_consulta.html'