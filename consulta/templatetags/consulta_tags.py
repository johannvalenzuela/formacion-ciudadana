from django import template
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

#modelos
from gestion_usuarios.models import Encargado

register = template.Library()


@register.filter
def is_autor_consulta(request, autor):
    '''
    Función para saber si el usuario es el autor de la consulta
    '''
    try:
        encargado= Encargado.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        return False
    else:
        if encargado==autor:
            return True
    return False

@register.filter
def is_finalizado_consulta(request, fecha_finalizacion):
    '''
    Función para saber si la consulta ya finalizó
    '''
    ahora = datetime.date(datetime.now())
    if ahora < fecha_finalizacion:
        return False

    return True