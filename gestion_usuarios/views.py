from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.shortcuts import redirect

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

#Modelos
from .models import Grupo, Encargado,RutAutorizados
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
        usuarios = RutAutorizados.objects.filter(grupo__in=grupoFuncion)
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
def agregarUsuarioFormView(request, pk_grupo):
    '''
    Muestra el formulario para agregar un usuario a un grupo en especifico
    '''
    grupo = Grupo.objects.get(pk=pk_grupo)
    args = {
        "grupo":grupo,
    }
    return render(request, "gestion_usuarios/usuario_add_form.html", args)


@login_required
@user_passes_test(funcionario_required)
def agregarUsuario(request, pk_grupo):
    '''
    agrega una relacion nueva de muchos es a muchos de un usuario con un grupo
    '''
    if request.method =="POST":
        nombreUsuario = request.POST.get("nombre")
        rutUsuario = request.POST.get("rut")
        grupo = Grupo.objects.get(pk=pk_grupo)
        usuarioNuevo = RutAutorizados.objects.create(rut=rutUsuario,nombre=nombreUsuario)

        usuarioNuevo.grupo.add(grupo)
        usuarioNuevo.save()
    return redirect('lista_usuarios', nombreGrupo=grupo.nombre)

@login_required
@user_passes_test(funcionario_required)
def removerUsuario(self, request, pk_grupo, pk_user):
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

