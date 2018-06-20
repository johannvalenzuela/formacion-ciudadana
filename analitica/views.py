from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

#modelos
from .models import Supervisor, Actividad
from gestion_usuarios import Encargado

class ActividadesListView(generic.ListView):
    '''
    Muestra la lista de actividades que puede ver el supervisor
    '''
    model= Actividad
    context_object_name = 'actividades'
    template_name = 'gestion_usuarios/actividades_lista.html'
    success_url = reverse_lazy('lista_actividades')

    def get_queryset(self):
        """Retorna las actividades del supervisor."""
        try:
            supervisor = Supervisor.objects.get(usuario=self.request.user)
        except ObjectDoesNotExist:
            return redirect('home')
        else:
            supervisados = Encargado.objects.filter(supervisor=supervisor)
            return Actividad.objects.filter(encargado__in=supervisados)
            
# class AsociarEncargadoView(generic.ListView):
#     template_name = 'gestion_usuarios/asociar_encargado.html'
#     success_url = reverse_lazy = ('lista_actividades')
