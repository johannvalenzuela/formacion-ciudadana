from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Consulta, Consulta_propuesta
from .forms import ConsultaPropuestaForm, ConsultaForm


class VisualizarConsultasView(generic.ListView):
    '''
    Muestra la vista de todas las consultas que el usuario puede ver
    '''
    template_name = 'consulta/visualizar_consultas.html'
    context_object_name = 'lista_consultas'

    def get_queryset(self):
        """Retorna las consultas."""
        return Consulta.objects.order_by('-fecha_inicio')

class CrearConsultaView(generic.CreateView):
    '''
    Muesta la vista para crear una consulta nueva
    '''
    form_class = ConsultaForm
    template_name = 'consulta/crear_consulta.html'
    success_url = reverse_lazy('visualizar_consultas')

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

class DetallesConsultaView(generic.DetailView):
    '''
    Muesta la vista de una consulta en especifico
    donde se mostraran los detalles de ella
    '''
    model = Consulta
    template_name = 'consulta/resultado_consulta.html'

    def obtenerConsulta(self, pk):
        print(pk)
        allData = Consulta.objects.all()
        print(allData)
        consultaId = allData.objects.get(pk=pk)
        print(consultaId)
        return consultaId

class ResponderConsultaView(generic.TemplateView):
    '''
    Muestra la vista para responder una consulta
    '''
    model = Consulta
    template_name = 'consulta/responder_consulta.html'
  
    def votar(request, propuesta_id):
        '''
        Funcion para realizar la votación
        '''
        propuesta = get_object_or_404(Consulta_propuesta, pk=propuesta_id)
        try:
            propuesta_seleccionada = propuesta.choice_set.get(pk=request.POST['eleccion'])
        except (KeyError, Consulta_propuesta.DoesNotExist):
            return render(request, 'consulta/responder_consulta.html',{
                'propuesta': propuesta,
                'error_message': "Usted no seleccionó ninguna propuesta",
            })
        else:
            propuesta_seleccionada.votos +=1
            propuesta_seleccionada.save()
        return HttpResponseRedirect(reverse('consulta:detalles_consulta', args=(propuesta.id,)))

class ConsultaDeleteView(generic.DeleteView):
    model = Consulta
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('visualizar_consultas')

# def ConsultaDeleteView(request, pk):
#     consulta = Consulta.objects.get(pk=pk)
#     consulta.delete()
#     return redirect('visualizar_consultas')