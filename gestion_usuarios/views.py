from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import messages


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
        try:
            usuarioNuevo= RutAutorizados.objects.get(rut=rutUsuario)
        except ObjectDoesNotExist:
            usuarioNuevo = RutAutorizados.objects.create(rut=rutUsuario,nombre=nombreUsuario)
        
        usuarioNuevo.grupo.add(grupo)
        usuarioNuevo.save()
    return redirect('lista_usuarios', nombreGrupo=grupo.nombre)

@login_required
@user_passes_test(funcionario_required)
def removerUsuarioView(request, pk_grupo, pk_usuario):
    '''
    Muestra el formulario para eliminar un usuario de un grupo en especifico
    '''
    grupo = Grupo.objects.get(pk=pk_grupo)
    usuario = RutAutorizados.objects.get(pk=pk_usuario)
    args = {
        "grupo":grupo,
        "usuario":usuario,
    }
    return render(request, "gestion_usuarios/usuarioGrupo_delete_form.html", args)

@login_required
@user_passes_test(funcionario_required)
def removerUsuario(request, pk_grupo, pk_usuario):
    '''
    elimina una relacion de muchos es a muchos de un usuario con un grupo
    '''
    if request.method =="POST":
        grupo = Grupo.objects.get(pk=pk_grupo)
        usuarioEliminar = RutAutorizados.objects.get(pk=pk_usuario)
            
        usuarioEliminar.grupo.remove(grupo)
        usuarioEliminar.save()
    return redirect('lista_usuarios', nombreGrupo=grupo.nombre)


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class AgregarGrupoView(generic.CreateView):
    '''
    Es la clase para agregar un grupo de un encargado en especifico.
    '''
    model = Grupo
    fields = ['nombre']
    template_name = 'gestion_usuarios/grupo_agregar_form.html'
    success_url = reverse_lazy('lista_grupos')

    def form_valid(self, form):
        '''
        Esta funcion se tira si el formulario es valido
        '''
        autor = Encargado.objects.get(usuario=self.request.user)
        establecimiento = autor.establecimiento
        titulo = form.instance.nombre
        try:
            grupoNuevo = Grupo.objects.get(nombre=titulo, autor=autor, establecimiento=establecimiento)
        except ObjectDoesNotExist:
            form.instance.autor = autor
            form.instance.establecimiento = establecimiento
        else:
            messages.error(self.request, 'El nombre que eligió ya existe')
            #return self.render_to_response(self.get_context_data(form=form))
            return redirect('lista_grupos')
            
        return super().form_valid(form)




    # def form_valid(self, form):
    #     grupo = form.save(commit=False)
    #     autorNuevo = Encargado.objects.get(usuario=self.request.user)
    #     establecimientoNuevo = autorNuevo.establecimiento

    #     grupo.autor = autorNuevo
    #     grupo.establecimiento = establecimientoNuevo
    #     return super(AgregarGrupoView, self).form_valid(form)



@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class EditarGrupoView(generic.UpdateView):
    '''
    Es la clase para editar un grupo de un encargado en especifico.
    '''
    model = Grupo
    fields = ['nombre',]
    template_name_suffix = '_editar_form'
    success_url = reverse_lazy('lista_grupos')

    def get_object(self, queryset=None):
        '''
        Esta función es para obtener el objeto a editar
        Se creo para que no funcionara si el grupo es alumnos o apoderados
        '''
        obj = Grupo.objects.get(pk=self.kwargs['pk'])
        if obj.nombre in "alumnos" or obj.nombre in "apoderados":
            return None
        return obj

    # def get_success_url(self):
    #     '''
    #     Es la función que se lanza una vez se realizo todo de forma correcta
    #     '''
	#     return reverse_lazy('lista_grupos', kwargs={'nombreGrupo': self.object.nombre})

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class EliminarGrupoView(generic.DeleteView):
    '''
    Es la clase para eliminar un grupo de un encargado en especifico.
    '''
    model = Grupo
    template_name_suffix = '_eliminar_form'
    success_url = reverse_lazy('lista_grupos')




