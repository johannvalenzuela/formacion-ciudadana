from django.shortcuts import render
from .models import Recurso, ValoracionRecurso
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from reportlab.pdfgen import canvas

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

        if not yaValoro(usuario, recurso):
            ValoracionRecurso.objects.create(usuario=usuario, recurso=recurso, valoracion=valoracion)
            recurso.setValoracion(valoracion)
            recurso.save()


def descargar(request, path):
    '''
        Funcion para descargar archivo PDF
    '''
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

