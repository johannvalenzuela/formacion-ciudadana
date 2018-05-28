from django.shortcuts import render
from .models import Recurso, ValoracionRecurso
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

    def yaValoro(usuario, recurso):
        '''
        Funcion que verifica si el usuario ya valoro anteriormente el recurso
        '''
        return ValoracionRecurso.objects.filter(usuario=usuario, recurso=recurso).exists()

    def valorar(request, recurso_id, autor_id, valoracion):
        '''
        Funcion para realizar la valoración
        '''
        usuario = settings.AUTH_USER_MODEL.objects.get(autor_id)
        recurso = Recurso.objects.get(id=recurso_id)
        if not yaValoro(usuario, recurso):
            ValoracionRecurso.objects.create(usuario=usuario, recurso=recurso, valoracion=valoracion)
            recurso.setValoracion(valoracion)
            recurso.save()

