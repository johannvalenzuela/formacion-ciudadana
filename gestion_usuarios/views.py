from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import ProfileForm

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

#Modelos
from .models import Grupo, Encargado,RutAutorizados
from autenticacion.models import Usuario


def funcionario_required(user):
    try:
        encargado = Encargado.objects.get(usuario=user)
    except ObjectDoesNotExist:
        return None
    return encargado


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


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class AgregarUsuarioGrupoView(generic.CreateView):
    '''
    Es la clase para agregar un grupo de un encargado en especifico.
    '''
    model = RutAutorizados
    fields = ['rut','nombre']
    template_name = 'gestion_usuarios/usuario_add_form.html'

    def form_valid(self, form):
        '''
        Esta funcion se tira si el formulario es valido
        '''
        try:
            grupo = Grupo.objects.get(pk=self.kwargs['pk_grupo'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Grupo no ingresado')
            return redirect('lista_grupos')
        else:
            try:
                usuarioExiste = RutAutorizados.objects.get(rut=form.instance.rut)
            except ObjectDoesNotExist:
                #si es que el usuario no existe se creo uno nuevo
                self.object = form.save(commit=False)
                self.object.save()
                form.instance.grupo.add(grupo)
            else:
                #sino se ocupa el ya existente
                self.object = usuarioExiste
                self.object.grupo.add(grupo)

        return self.get_success_url()
        
    def get_success_url(self):
        grupo = Grupo.objects.get(pk=self.kwargs['pk_grupo'])
        return redirect('lista_usuarios', nombreGrupo=grupo.nombre)

    def get(self, request, pk_grupo):
        grupo = Grupo.objects.get(pk=pk_grupo)
        args = {
            "grupo": grupo,
        }
        return render(request, "gestion_usuarios/usuario_add_form.html", args)

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class EliminarUsuarioGrupoView(generic.DeleteView):
    '''
    Es la clase para eliminar un grupo de un encargado en especifico.
    '''
    model = RutAutorizados
    template_name = 'gestion_usuarios/usuarioGrupo_delete_form.html'
    pk_url_kwarg = 'pk_usuario'
 
    def get_success_url(self):
        grupo = Grupo.objects.get(pk=self.kwargs['pk_grupo'])
        return redirect('lista_usuarios', nombreGrupo=grupo.nombre)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        grupo = Grupo.objects.get(pk=self.kwargs['pk_grupo'])
        self.object.grupo.remove(grupo)
        return self.get_success_url()

    def get(self, request, pk_grupo, pk_usuario):
        grupo = Grupo.objects.get(pk=pk_grupo)
        usuario = RutAutorizados.objects.get(pk=pk_usuario)
        args = {
            "grupo":grupo,
            "usuario":usuario,
        }
        return render(request, "gestion_usuarios/usuarioGrupo_delete_form.html", args)
        

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
            grupoNuevo = Grupo.objects.get(nombre=titulo, establecimiento=establecimiento)
        except ObjectDoesNotExist:
            form.instance.autor = autor
            form.instance.establecimiento = establecimiento
        else:
            messages.error(self.request, 'El nombre del grupo que eligió ya existe')
            return redirect('lista_grupos')
            
        return super().form_valid(form)



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


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(funcionario_required), name='get')
class EliminarGrupoView(generic.DeleteView):
    '''
    Es la clase para eliminar un grupo de un encargado en especifico.
    '''
    model = Grupo
    template_name_suffix = '_eliminar_form'
    success_url = reverse_lazy('lista_grupos')


class ProfileView(generic.DetailView):
    '''
    Muesta la vista del profile del usuario
    '''
    model = Usuario
    context_object_name = 'usuario'
    template_name = 'gestion_usuarios/usuario_profile.html'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generic.UpdateView):
    '''
    Muesta la vista para eliminar valores del profile del usuario 
    '''
    model = Usuario
    context_object_name = 'usuario'
    form_class = ProfileForm
    template_name = 'gestion_usuarios/usuario_profile_editar.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    


