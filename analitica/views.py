from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

#modelos
from .models import Supervisor, Actividad
from gestion_usuarios.models import Encargado

def supervisor_required(user):
    try:
        supervisor = Supervisor.objects.get(usuario=user)
    except ObjectDoesNotExist:
        return None
    
    return supervisor

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(supervisor_required), name='get')
class ActividadesListView(generic.ListView):
    '''
    Muestra la lista de actividades que puede ver el supervisor
    '''
    model= Actividad
    context_object_name = 'actividades'
    template_name = 'analitica/actividades_lista.html'
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

