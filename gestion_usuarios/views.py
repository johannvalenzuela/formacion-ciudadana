from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render 

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
class ListaUsuariosView(generic.ListView):
    '''
    Vista de la lista de usuarios de un grupo de un encargado.
    '''
    template_name = 'gestion_usuarios/lista_usuarios.html'

    def get(self, request, nombreGrupo):
        autor = Encargado.objects.get(usuario=self.request.user)
        grupo = Grupo.objects.get(nombre=nombreGrupo, autor=autor)
        
        grupoFuncion = Grupo.objects.filter(nombre=nombreGrupo, autor=autor)
        usuarios = Usuario.objects.filter(grupo__in=grupoFuncion)
        args = {
            "grupo": grupo,
            "lista_usuarios": usuarios,
        }
        return render(request,'gestion_usuarios/lista_usuarios.html',args )


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

@login_required
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

