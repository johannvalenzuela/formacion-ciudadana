from django.shortcuts import render
from .models import Recurso, ValoracionRecurso
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

class BibliotecaView(generic.ListView):
    template_name = 'biblioteca_digital/principal.html'
    context_object_name = 'lista_recursos'
    form_class = 'BiblitecaForm'

    def get_queryset(self):
        """Retorna los 5 recursos mejor valorados."""
        return Recurso.objects.order_by('valoracionTotal')[:5]

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

    def valorar(request, pk):
        '''
        Funcion para realizar la valoración
        '''
        recurso = get_object_or_404(Recurso,pk=pk)
        user = request.user
        valoracion = request.POST['valoracion']

        if not yaValoro(user, recurso):
            ValoracionRecurso.objects.create(usuario=user, recurso=recurso, valoracion=valoracion)
            recurso.setValoracion(valoracion)
            recurso.save()
            return HttpResponse(True)
        return HttpResponse(False)

def descargar(request, pk):
    '''
    Funcion para descargar archivo PDF
    '''
    recurso = Recurso.objects.get(pk=pk)
    path= 'recursos/' + recurso.titulo
    archivo = recurso.archivo
    filename = os.path.join(settings.MEDIA_ROOT, path)
    content = archivo.read()
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+recurso.titulo+".pdf"
    return response


