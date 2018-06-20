from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

#modelos
from gestion_usuarios.models import Encargado

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class PoliticaPrivacidad(TemplateView):
    template_name = 'registration/politica_privacidad.html'

def login_success(request):
    """
    Es la vista para redireccionar a los usuarios cuando se autentifican
    """
    usuario = request.user
    try:
        encargado = Encargado.objects.get(usuario=usuario)
    except ObjectDoesNotExist:
        try:
            #supervisor = Supervisor.objects.get(usuario=usuario)
        except ObjectDoesNotExist:
            #si es supervisor redirecciona
            return redirect("visualizar_consultas")
        else:
            #si no es ni encargado ni supervisor redirecciona a las consultas
            return redirect("visualizar_actividades")
    #si es encargado redirecciona a la biblioteca digital    
    return redirect("biblioteca_digital")

        
    
