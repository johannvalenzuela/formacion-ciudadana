from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import ObjectDoesNotExist
from .models import Supervisor

def supervisor_required(user):
    try:
        supervisor = Supervisor.objects.get(usuario=user)
    except ObjectDoesNotExist:
        return None
    
    return supervisor