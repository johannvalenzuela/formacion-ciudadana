from django.shortcuts import render
from .models import Recurso
from django.views import generic

class BibliotecaView(generic.ListView):
    template_name = 'biblioteca_digital/principal.html'
    context_object_name = 'lista_recursos'
    form_class = 'BiblitecaForm'

    def get_queryset(self):
        """Retorna los 5 recursos mejor valorados."""
        return Recurso.objects.order_by('valoracion')[:5]

class RecursoDetailView(generic.DetailView):
    model = Recurso
    template_name = 'biblioteca_digital/recurso.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context