from django import template

register = template.Library()

from django.core.exceptions import ObjectDoesNotExist

#modelos
from analitica.models import Supervisor
from gestion_usuarios.models import Encargado

@register.filter
def funcionario_required(request):
    '''
    Función para mostrar los links del navbar de los funcionarios.
    '''
    if request.user.is_anonymous:
        return False

    try:
        encargado = Encargado.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        try:
            supervisor = Supervisor.objects.get(usuario=request.user)
        except ObjectDoesNotExist:
            return False
        else:
            return True
    return True

@register.filter
def encargado_required(request):
    '''
    Función para mostrar los links del navbar de los encargados.
    '''
    if request.user.is_anonymous:
        return False

    try:
        encargado = Encargado.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        return False
    
    return True

@register.filter
def supervisor_required(request):
    '''
    Función para mostrar los links del navbar de los supervisores.
    '''
    if request.user.is_anonymous:
        return False

    try:
        supervisor = Supervisor.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        return False
    
    return True