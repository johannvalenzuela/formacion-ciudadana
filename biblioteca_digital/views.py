from django.shortcuts import render
from .models import Recurso, ValoracionRecurso
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from autenticacion.decorators import funcionario_required
from django.utils.decorators import method_decorator
from .forms import  ComentarioForm, RecursoForm

@method_decorator(funcionario_required, name='get' )
class BibliotecaView(generic.ListView):
    template_name = 'biblioteca_digital/principal.html'
    context_object_name = 'lista_recursos'

    def get_queryset(self):
        """Retorna los 5 recursos mejor valorados."""
        return Recurso.objects.order_by('valoracionTotal')[:5]

@method_decorator(funcionario_required, name='get')
class RecursoDetailView(generic.DetailView):
    model = Recurso
    template_name = 'biblioteca_digital/recurso.html'
    form_class = 'ComentarioForm'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def valorar(request, pk):
        '''
        Funcion para realizar la valoración
        '''
        recurso = get_object_or_404(Recurso,pk=pk)
        user = request.user
        valoracion = request.POST['valoracion']
        yaValoro = ValoracionRecurso.objects.filter(usuario=user.pk, recurso=recurso.pk).exists()
        if yaValoro:
            return HttpResponse(False)
        ValoracionRecurso.objects.create(usuario=user, recurso=recurso, valoracion=valoracion)
        recurso.setValoracion(valoracion)
        recurso.save()
        return HttpResponse(True)

@funcionario_required
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

@method_decorator(funcionario_required, name='get' ) 
class CrearRecursoView(generic.CreateView): 
    form_class = RecursoForm 
    success_url = reverse_lazy('biblioteca_digital') 
    template_name = 'biblioteca_digital/recurso_nuevo.html' 

class RecursoUpdateView(generic.UpdateView):
    model = Recurso
    template_name = 'biblioteca_digital/editar-recurso.html'
    fields = ['titulo','descripcion', 'imagen_descriptiva', 'tema', 'archivo']
    # form_class = RecursoForm
    success_url = reverse_lazy('biblioteca_digital')

class RecursoDeleteView(generic.DeleteView):
    model = Recurso
    template_name = 'biblioteca_digital/eliminar-recurso.html'
    # fields = ['titulo','descripcion', 'imagen_descriptiva', 'tema', 'archivo']
    form_class = RecursoForm
    success_url = reverse_lazy('biblioteca_digital')
