from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def funcionario_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator para verificar que en las views si esta logeado el usuario encargado supervisor o admin
    Redirecciona al login si es que no es así
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_funcionario,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator