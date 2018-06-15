from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import ConsultaPropuestaForm, ConsultaForm
from django.core.exceptions import ObjectDoesNotExist

#modelos
from .models import Consulta, ConsultaPropuesta
from gestion_usuarios.models import Encargado

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

def funcionario_required(user):
    try:
        encargado = Encargado.objects.get(usuario=user)
    except ObjectDoesNotExist:
        return None
    return encargado


class VisualizarConsultasView(generic.ListView):
    '''
    Muestra la vista de todas las consultas que el usuario puede ver
    '''
    template_name = 'consulta/consulta_lista.html'
    context_object_name = 'lista_consultas'

    def get_queryset(self):
        """Retorna las consultas."""
        return Consulta.objects.order_by('-fecha_inicio')

class DetallesConsultaView(generic.DetailView):
    '''
    Muesta la vista de una consulta en especifico
    donde se mostraran los detalles de ella
    '''
    model = Consulta
    template_name = 'consulta/consulta_detalles.html'


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class CrearConsultaView(generic.CreateView):
    '''
    Muesta la vista para crear una consulta nueva
    '''
    form_class = ConsultaForm
    template_name = 'consulta/create_form.html'
    success_url = reverse_lazy('visualizar_consultas')


@method_decorator(login_required, name='get' )
class ResponderConsultaView(generic.TemplateView):
    '''
    Muestra la vista para responder una consulta
    '''
    model = Consulta
    template_name = 'consulta/consulta_votar.html'
  
    def votar(request, propuesta_id):
        '''
        Funcion para realizar la votación
        '''
        propuesta = get_object_or_404(ConsultaPropuesta, pk=propuesta_id)
        try:
            propuesta_seleccionada = propuesta.choice_set.get(pk=request.POST['eleccion'])
        except (KeyError, ConsultaPropuesta.DoesNotExist):
            return render(request, 'consulta/responder_consulta.html',{
                'propuesta': propuesta,
                'error_message': "Usted no seleccionó ninguna propuesta",
            })
        else:
            propuesta_seleccionada.votos +=1
            propuesta_seleccionada.save()
        return HttpResponseRedirect(reverse('consulta:detalles_consulta', args=(propuesta.id,)))

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class ConsultaDeleteView(generic.DeleteView):
    model = Consulta
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('visualizar_consultas')


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class ConsultaUpdateView(generic.UpdateView):
    model = Consulta
    fields = ['titulo','descripcion','fecha_inicio','fecha_finalizacion',]
    template_name = 'consulta/consulta_update_form.html'

    def get_success_url(self):
	    return reverse_lazy('detalles_consulta', kwargs={'pk': self.object.pk})



#-----------------------------------------PROPUESTAS-----------------------------------

class PropuestaConsultaVisualizarView(generic.DetailView):
    '''
    Muestra la vista para ver una propuesta(respuesta) de una consulta
    '''
    model = ConsultaPropuesta
    template_name = 'consulta/propuesta_detalles.html'


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class PropuestaConsultaCreateView(generic.CreateView):
    '''
    Muestra un formulario para la creación de una alternativa de una consulta
    en específica.
    '''
    form_class = ConsultaPropuestaForm
    template_name = "consulta/propuesta_create_form.html"

    def form_valid(self, form):  
        try:
            consulta = Consulta.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Consulta no encontrada')
            return redirect('')
        else:
            form.instance.consulta = consulta
            form.instance.autor = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        consulta = Consulta.objects.get(pk=self.kwargs['pk'])
        return redirect('detalles_consulta', pk=consulta)


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class PropuestaConsultaUpdateView(generic.UpdateView):
    '''
    Es la clase para editar un grupo de un encargado en especifico.
    '''
    form_class = ConsultaPropuestaForm
    template_name = "consulta/propuesta_update_form.html"

    def get_success_url(self):
        propuesta = ConsultaPropuesta.objects.get(pk=self.kwargs['pk'])
        return redirect('visualizar_propuesta', pk=propuesta)


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get' )
class PropuestaConsultaDeleteView(generic.DeleteView):
    '''
    Es la clase para eliminar un grupo de un encargado en especifico.
    '''
    model = ConsultaPropuesta
    template_name = "consulta/propuesta_confirm_delete.html"

    def get_success_url(self):
        propuesta = ConsultaPropuesta.objects.get(pk=self.kwargs['pk'])
        return redirect('visualizar_propuesta', pk=propuesta)




