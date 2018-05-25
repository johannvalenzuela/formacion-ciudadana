from django.shortcuts import render
from django.views.generic import TemplateView

class BibliotecaView(TemplateView):
    template_name = 'biblioteca_digital/principal.html'
    