from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('nombre', 'apellido_paterno','apellido_materno', 'email', 
                    'fecha_nacimiento')
    
    fecha_nacimiento= forms.CharField(
        label=_("fecha de nacimiento"),
        widget=forms.DateInput,
    )

    error_messages = {
        'password_mismatch': _("Los dos campos de contraseña no coinciden."),
    }
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("confirmación de contraseña"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Ingrese la misma contraseña que antes, para verificación."),
    )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = UserChangeForm.Meta.fields

    