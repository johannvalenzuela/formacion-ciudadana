from django.shortcuts import render
from .models import Recurso, ValoracionRecurso, ComentarioRecurso
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from autenticacion.decorators import funcionario_required
from django.utils.decorators import method_decorator
from .forms import RecursoForm
from django.shortcuts import redirect

@method_decorator(funcionario_required, name='get' )
class BibliotecaView(generic.ListView):
    template_name = 'biblioteca_digital/principal.html'
    context_object_name = 'lista_recursos'
    paginate_by = 10

    def get_queryset(self):
        """Retorna los recursos ordenados desde el más valorado al menos."""
        return Recurso.objects.order_by('valoracionTotal')

@method_decorator(funcionario_required, name='get')
class RecursoDetailView(generic.DetailView):
    model = Recurso
    template_name = 'biblioteca_digital/recurso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = ComentarioRecurso.objects.filter(recurso=self.object.pk).order_by('-fecha_creacion')
        return context

    @funcionario_required
    def comentar(request, pk):
        '''
        Funcion para realizar un comentario
        '''
        if request.method == "POST":
            autor = request.user
            comentarioActual = request.POST.get('comentario')
            recursoActual = get_object_or_404(Recurso,pk=pk)
            comentarioNuevo = ComentarioRecurso.objects.create(
                autorComentario = request.user,
                recurso = recursoActual,
                comentario = comentarioActual
            )
        return redirect('recurso-detail', pk=pk)

    @funcionario_required
    def valorar(request, pk):
        '''
        Funcion para realizar la valoración
        '''
        if request.method == "POST":
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
        return reverse_lazy('recurso-detail', kwargs={'pk': pk})


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
    template_name = 'biblioteca_digital/recurso_create_form.html'
    success_url = reverse_lazy('biblioteca_digital')

    def form_valid(self, form):  
        form.instance.autor = self.request.user
        form.save()
        return super().form_valid(form)

@method_decorator(funcionario_required, name='get')
class RecursoUpdateView(generic.UpdateView):
    model = Recurso
    fields = ['titulo', 'descripcion','tema','imagen_descriptiva','archivo',]
    template_name_suffix = '_update_form'

    def get_success_url(self):
	    return reverse_lazy('recurso-detail', kwargs={'pk': self.object.pk})
    

@method_decorator(funcionario_required, name='get')
class RecursoDeleteView(generic.DeleteView):
    model = Recurso
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('biblioteca_digital')
        

        