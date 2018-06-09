from django.views import generic
from django.urls import reverse_lazy

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

#Modelos
from .models import Grupo, Encargado
from autenticacion.models import Usuario

def funcionario_required(usuario):
    return Encargado.objects.get(usuario=usuario)

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class ListaAlumnosView(generic.ListView):
    '''
    Vista de la lista de alumnos de un encargado.
    '''
    template_name = 'gestion_usuarios/lista_usuarios.html'
    context_object_name = 'lista_alumnos'
    paginate_by = 20

    def get_queryset(self):
        """Retorna los alumnos."""
        autor = Encargado.objects.get(usuario=self.request.user)
        grupo = Grupo.objects.filter(nombre="alumnos",autor=autor)
        return Usuario.objects.filter(grupo__in=grupo)


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class ListaApoderadosView(generic.ListView):
    '''
    Vista de la lista de apoderados de un encargado.
    '''
    template_name = 'gestion_usuarios/lista_usuarios.html'
    context_object_name = 'lista_apoderados'
    paginate_by = 20

    def get_queryset(self):
        """Retorna los alumnos."""
        autor = Encargado.objects.get(usuario=self.request.user)
        grupo = Grupo.objects.filter(nombre="apoderados",autor=autor)
        return Usuario.objects.filter(grupo__in=grupo)

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class ListaGruposView(generic.ListView):
    '''
    Vista de la lista de grupos de un encargado.
    '''
    template_name = 'gestion_usuarios/lista_grupos.html'
    context_object_name = 'lista_grupos'
    paginate_by = 20

    def get_queryset(self):
        """Retorna los grupos."""
        autor = Encargado.objects.get(usuario=self.request.user)
        return Grupo.objects.filter(autor=autor)


# @method_decorator(funcionario_required, name='get' )
# class CrearUsuarioView(generic.CreateView): 
#     #form_class = RecursoForm 
#     template_name = 'gestion_usuarios/usuario_create_form.html'
#     success_url = reverse_lazy('biblioteca_digital')


# @method_decorator(funcionario_required, name='get')
# class UsuarioDeleteView(generic.DeleteView):
#     model = Usuario
#     template_name_suffix = '_confirm_delete'
#     success_url = reverse_lazy('biblioteca_digital')