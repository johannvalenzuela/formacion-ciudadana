from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import ObjectDoesNotExist

#modelos
from analitica.models import Supervisor
from gestion_usuarios.models import Encargado

def funcionario_required(user):
    try:
        encargado = Encargado.objects.get(usuario=user)
    except ObjectDoesNotExist:
        try:
            supervisor = Supervisor.objects.get(usuario=user)
        except ObjectDoesNotExist:
            return None
        else:
            return supervisor
    return encargado


def encargado_required(user):
    try:
        encargado = Encargado.objects.get(usuario=user)
    except ObjectDoesNotExist:
        return None
    
    return encargado