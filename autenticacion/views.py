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
    Redirects users based on whether they are in the admins group
    """
    usuario = request.user
    try:
        encargado = Encargado.objects.get(usuario=usuario)
    except ObjectDoesNotExist:
        return redirect("home")
    else:
        return redirect("biblioteca_digital")

        
    
