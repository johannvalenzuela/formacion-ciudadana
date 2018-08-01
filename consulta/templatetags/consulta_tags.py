from django import template
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

#modelos
from gestion_usuarios.models import Encargado, RutAutorizados
from consulta.models import ConsultaRespuesta

register = template.Library()


@register.filter
def is_autor_consulta(request, autor):
    '''
    Función para saber si el usuario es el autor de la consulta
    '''
    if request.user.is_anonymous:
        return False
    try:
        encargado= Encargado.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        return False
    else:
        if encargado==autor:
            return True
    return False

@register.filter
def is_anonimo(request):
    '''
    Función para saber si el usuario no tiene cuenta
    '''
    if request.user.is_anonymous:
        return True
    return False

@register.filter
def is_finalizado_consulta(request, fecha_finalizacion):
    '''
    Función para saber si la consulta ya finalizó
    '''
    ahora = datetime.date(datetime.now())
    if ahora > fecha_finalizacion:
        return False

    return True

@register.filter
def puede_votar_consulta(request, consulta):
    '''
    Función para saber si el usuario puede votar en la consulta
    '''
    if request.user.is_anonymous:
        return True

    if not request.user.rut:
        return True
        
    rut_user = request.user.rut
    try:
        ConsultaRespuesta.objects.get(consulta=consulta ,rut=rut_user)
    except ObjectDoesNotExist:
        #se verifica si es una elección libre(ciudadana) o tiene restricciones
        grupos = consulta.grupo.all()
        if grupos.count() > 0:
            autorizados = RutAutorizados.objects.filter(grupo__in=grupos)
                
            for autorizado in autorizados:
                if autorizado.rut == rut_user:
                    return True
                    break
        else:
            return True   
    
    return False