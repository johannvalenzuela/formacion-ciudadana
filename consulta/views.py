from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import ConsultaPropuestaForm, ConsultaForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

#modelos
from .models import Consulta, ConsultaPropuesta, ConsultaRespuesta
from gestion_usuarios.models import Encargado, RutAutorizados
from autenticacion.models import Usuario
from analitica.models import Actividad, Supervisor

#decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from gestion_usuarios.decorators import encargado_required


class VisualizarConsultasView(generic.ListView):
    '''
    Muestra la vista de todas las consultas que el usuario puede ver
    '''
    template_name = 'consulta/consulta_lista.html'
    context_object_name = 'lista_consultas'

    def get_queryset(self):
        """Retorna las consultas."""
        #Si el usuario es anonimo se muestran todos los grupos que no tengan grupos
        if self.request.user.is_anonymous:
            return Consulta.objects.filter(grupo=None).order_by('fecha_inicio')
        
        try:
            supervisor=Supervisor.objects.get(usuario=self.request.user)
        except ObjectDoesNotExist:
            try:
                encargado = Encargado.objects.get(usuario=self.request.user)
            except ObjectDoesNotExist:
                try:
                    autorizados = RutAutorizados.objects.get(rut= self.request.user.rut)
                except ObjectDoesNotExist:
                    #si no tiene rut solo se le muestran las consultas ciudadanas
                    return Consulta.objects.filter(grupo=None).order_by('fecha_inicio')
                else:
                    return Consulta.objects.filter(Q(grupo__in=autorizados.grupo.all()) | Q(grupo=None)).order_by('-fecha_inicio')
            else:
                #si el usuario es encargado se muestran los grupos creados por el
                #y las consultas ciudadanas
                return Consulta.objects.filter(Q(autor=encargado) | Q(grupo=None)).order_by('fecha_inicio')
          
        else:
            #si el usuario es supervisor se muestran los grupos creados por sus encargados
            #y las consultas ciudadanas
            encargados = Encargado.objects.filter(supervisor=supervisor)
            return Consulta.objects.filter(Q(autor__in=encargados) | Q(grupo=None)).order_by('fecha_inicio')
        

        

class DetallesConsultaView(generic.DetailView):
    '''
    Muesta la vista de una consulta en especifico
    donde se mostraran los detalles de ella
    '''
    model = Consulta
    template_name = 'consulta/consulta_detalles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['propuestas'] = ConsultaPropuesta.objects.filter(consulta=self.object.pk)
        return context

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class CrearConsultaView(generic.CreateView):
    '''
    Muesta la vista para crear una consulta nueva
    '''
    form_class = ConsultaForm
    template_name = 'consulta/consulta_create_form.html'
    success_url = reverse_lazy('visualizar_consultas')

    def form_valid(self, form):
        encargado = Encargado.objects.get(usuario=self.request.user)
        try:
            form.instance.autor = encargado
            form.save()
        finally:
            Actividad.objects.create(
                titulo="%s" % (form.instance.titulo),
                tipo="Consulta",
                link="detalles_consulta",
                link_pk=form.instance.pk,
                encargado=encargado,
            )  
        
        return super().form_valid(form)


@method_decorator(login_required, name='get' )
@method_decorator(login_required, name='post' )
class ResponderConsultaView(generic.TemplateView):
    '''
    Muestra la vista para responder una consulta
    '''
    model = Consulta
    template_name = 'consulta/consulta_votar.html'
  

    def post(self, request, pk):
        '''
        vista para votar en una consulta
        '''
        puedeVotar=False
        if request.method == 'POST':
            #primero se obtienen la consulta, el votante y la alternativa que marco
            consulta = get_object_or_404(Consulta, pk=pk)
            
                #se valida de que exista rut y numero de documento
            if request.user.rut or request.user.num_documento:
                try:
                    votante = Usuario.objects.get(rut=request.user.rut, num_documento=request.user.num_documento)
                except ObjectDoesNotExist:
                    return redirect('datos_faltantes', pk_consulta=pk)
            else:
                return redirect('datos_faltantes', pk_consulta=pk)
           
            propuesta = get_object_or_404(ConsultaPropuesta, pk=request.POST.get('eleccion'))
            

            #antes de seguir se verifica si ya voto anteriormente
            try:
                ConsultaRespuesta.objects.get(consulta=consulta ,rut=votante.rut)
            except ObjectDoesNotExist:
                #segundo se verifica si es una elección libre(ciudadana) o tiene restricciones
                grupos = consulta.grupo.all()
                if grupos.count() > 0:
                    autorizados = RutAutorizados.objects.filter(grupo__in=grupos)
                        
                    for autorizado in autorizados:
                        if autorizado.rut == votante.rut:
                            puedeVotar=True
                            break
                else:
                    puedeVotar=True            
                finalizado=True
                if puedeVotar:
                    #se verifica que la votación no haya finalizado
                    if datetime.now < consulta.fecha_finalizacion:
                        finalizado=False

                        #por último el usuario realiza la votación
                        try:
                            ConsultaRespuesta.objects.create(
                            rut = votante.rut,
                            consulta = consulta,
                            consulta_propuesta = propuesta,
                            )
                        finally:
                            propuesta.votos+=1
                            propuesta.save()
            
            else:
                messages.error(request, 'usuario ya realizó la votación anteriormente')
                return self.get_success_url()
            
            

        if puedeVotar:
            if not finalizado:
                messages.success(request, 'Votación realizada con éxito!')
            else:
                messages.success(request, 'La votacion no pudo ser realizada porque ya terminó')
        else:
            messages.error(request, 'La votación no pudo ser realizada')

        return self.get_success_url()
                
    def get_success_url(self):
        return redirect('detalles_consulta', pk=self.kwargs['pk'])
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consulta'] = get_object_or_404(Consulta, pk=kwargs['pk'])
        context['propuestas'] = ConsultaPropuesta.objects.filter(consulta=kwargs['pk'])
        return context

    
@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class ConsultaDeleteView(generic.DeleteView):
    model = Consulta
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('visualizar_consultas')


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class ConsultaUpdateView(generic.UpdateView):
    model = Consulta
    fields = ['titulo','descripcion','fecha_inicio','fecha_finalizacion',]
    template_name = 'consulta/consulta_update_form.html'

    def get_success_url(self):
	    return reverse_lazy('detalles_consulta', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='get' )
class DatosFaltantesView(generic.UpdateView):
    '''
    Muesta la vista agregar el rut y el numero de documento si el usuario intenta votar
    y no los ha ingresado
    '''
    model = Usuario
    fields = ['rut', 'num_documento']
    template_name = 'consulta/consulta_datos_faltantes.html'

    def get_object(self):
        usuario = get_object_or_404(Usuario, pk=self.request.user.pk)
        return usuario
    
    def form_valid(self, form):
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('consulta_votar', pk=self.kwargs['pk_consulta'])
#-----------------------------------------PROPUESTAS-----------------------------------

class PropuestaConsultaVisualizarView(generic.DetailView):
    '''
    Muestra la vista para ver una propuesta(respuesta) de una consulta
    '''
    model = ConsultaPropuesta
    template_name = 'consulta/propuesta_detalles.html'


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class PropuestaConsultaCreateView(generic.CreateView):
    '''
    Muestra un formulario para la creación de una alternativa de una consulta
    en específica.
    '''
    model = ConsultaPropuesta
    form_class = ConsultaPropuestaForm
    template_name = "consulta/propuesta_create_form.html"

    def form_valid(self, form):  
        try:
            #Primero se valida de que la consulta sea valida
            consulta = Consulta.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Consulta no encontrada')
            return redirect('')
        else:
            #Despues se valida de que no exista otra propuesta con el mismo nombre
            validacionNombre=False
            try:
                propuestas = ConsultaPropuesta.objects.get(titulo=form.instance.titulo,consulta=consulta)
            except ObjectDoesNotExist:
                #se verifica que la votación no haya finalizado
                if datetime.now < consulta.fecha_finalizacion:
                    form.instance.consulta = consulta
                    form.instance.autor = self.request.user
                    form.save()
            else:
                messages.error(self.request, 'No se pueden repetir los nombres de las propuestas')
        return self.get_success_url()

    def get_success_url(self):
        return redirect('detalles_consulta', pk=self.kwargs['pk'])


@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class PropuestaConsultaUpdateView(generic.UpdateView):
    '''
    Es la clase para editar un grupo de un encargado en especifico.
    '''
    model = ConsultaPropuesta
    form_class = ConsultaPropuestaForm
    template_name = "consulta/propuesta_update_form.html"

    def get_success_url(self):
        return redirect('visualizar_propuesta', pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.save()
        return self.get_success_url()

@method_decorator(login_required, name='get' )
@method_decorator(user_passes_test(encargado_required), name='get' )
class PropuestaConsultaDeleteView(generic.DeleteView):
    '''
    Es la clase para eliminar un grupo de un encargado en especifico.
    '''
    model = ConsultaPropuesta
    template_name = "consulta/propuesta_confirm_delete.html"
    success_url = reverse_lazy("visualizar_consultas")




