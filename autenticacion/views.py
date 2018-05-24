from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class PoliticaPrivacidad(TemplateView):
    template_name = 'registration/politica_privacidad.html'