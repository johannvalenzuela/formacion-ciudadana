from django.shortcuts import render
from django.views import generic
from .models import Consulta

# Create your views here.
class VisualizarConsultasView(generic.ListView):
    template_name = 'consulta/visualizar_consultas.html'
    context_object_name = 'lista_consultas'

    def get_queryset(self):
        """Retorna las consultas."""
        return Consulta.objects.all()