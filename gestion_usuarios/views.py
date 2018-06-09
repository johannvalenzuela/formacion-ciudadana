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
    context_object_name = 'lista_usuarios'
    paginate_by = 20

    def get_queryset(self):
        """Retorna los alumnos."""
        autor = Encargado.objects.get(usuario=self.request.user)
        grupo = Grupo.objects.filter(nombre="alumnos",autor=autor)
        return Usuario.objects.filter(grupo__in=grupo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        autor = Encargado.objects.get(usuario=self.request.user)
        context['grupo'] = Grupo.objects.get(nombre='alumnos', autor=autor)
        return context


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class ListaApoderadosView(generic.ListView):
    '''
    Vista de la lista de apoderados de un encargado.
    '''
    template_name = 'gestion_usuarios/lista_usuarios.html'
    context_object_name = 'lista_usuarios'
    paginate_by = 20

    def get_queryset(self):
        """Retorna los apoderados."""
        autor = Encargado.objects.get(usuario=self.request.user)
        grupo = Grupo.objects.filter(nombre="apoderados",autor=autor)
        return Usuario.objects.filter(grupo__in=grupo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        autor = Encargado.objects.get(usuario=self.request.user)
        context['grupo'] = Grupo.objects.get(nombre='apoderados', autor=autor)
        return context

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

@user_passes_test(funcionario_required)
def agregarUsuario(request):
    '''
    agrega una relacion nueva de muchos es a muchos de un usuario con un grupo
    '''
    if request.method =="POST":
        grupoAIngresar = request.method.POST.get('grupo')
        usuarioAIngresar = request.method.POST.get('usuario')
        
        grupo = Grupo.objects.get(nombre=grupoAIngresar, autor=request.user)
        usuario = Usuario.objects.get(nombre=usuarioAIngresar, autor=request.user)
        
        usuario.grupo.add(grupoAIngresar)
        usuario.save()
    return redirect(grupoAIngresar)

@user_passes_test(funcionario_required)
def removerUsuario(request):
    '''
    elimina una relacion de muchos es a muchos de un usuario con un grupo
    '''
    if request.method =="POST":
        grupoAIngresar = request.method.POST.get('grupo')
        usuarioAIngresar = request.method.POST.get('usuario')
        
        grupo = Grupo.objects.get(nombre=grupoAIngresar, autor=request.user)
        usuario = Usuario.objects.get(nombre=usuarioAIngresar, autor=request.user)
        
        usuario.grupo.remove(grupoAIngresar)
        usuario.save()
    return redirect(grupoAIngresar)

