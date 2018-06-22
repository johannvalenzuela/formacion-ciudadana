from django import template
from django.core.exceptions import ObjectDoesNotExist

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