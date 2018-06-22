from django.contrib import admin
from .models import Servicio_Local_Educacion
from .models import Departamento_Provincial_Educacion
from .models import Establecimiento
from .models import Asignatura
from .models import Encargado
from .models import Grupo
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

#aqui comienza las librerias importadas del response_add
import json
import re
from urllib.parse import quote as urlquote
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin import helpers, widgets
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import quote
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _ 



admin.site.register(Servicio_Local_Educacion)
admin.site.register(Departamento_Provincial_Educacion)
admin.site.register(Establecimiento)
admin.site.register(Asignatura)


IS_POPUP_VAR = '_popup'


class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('usuario','asignatura', 'establecimiento')
    search_fields = ('usuario','asignatura', 'establecimiento')

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        preserved_filters = self.get_preserved_filters(request)
        obj_url = reverse(
            'admin:%s_%s_change' % (opts.app_label, opts.model_name),
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        #se crean los grupos por defecto del encargado
        try:
            Grupo.objects.get(nombre="alumnos", establecimiento=obj.establecimiento)
        except ObjectDoesNotExist:
            Grupo.objects.create(
            nombre="alumnos",
            autor=obj,
            establecimiento=obj.establecimiento
            )
             
        try:
            Grupo.objects.get(nombre="apoderados", establecimiento=obj.establecimiento)
        except ObjectDoesNotExist:
            Grupo.objects.create(
            nombre="apoderados",
            autor=obj,
            establecimiento=obj.establecimiento
            )
            
        
        # Add a link to the object's change form if the user can edit the obj.
        if self.has_change_permission(request, obj):
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = str(obj)
        msg_dict = {
            'name': opts.verbose_name,
            'obj': obj_repr,
        }
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.

        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            popup_response_data = json.dumps({
                'value': str(value),
                'obj': str(obj),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })

        elif "_continue" in request.POST or (
                # Redirecting after "Save as new".
                "_saveasnew" in request.POST and self.save_as_continue and
                self.has_change_permission(request, obj)
        ):
            msg = _('The {name} "{obj}" was added successfully.')
            if self.has_change_permission(request, obj):
                msg += ' ' + _('You may edit it again below.')
            self.message_user(request, format_html(msg, **msg_dict), messages.SUCCESS)
            if post_url_continue is None:
                post_url_continue = obj_url
            post_url_continue = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts},
                post_url_continue
            )
            return HttpResponseRedirect(post_url_continue)

        elif "_addanother" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may add another {name} below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(
                _('The {name} "{obj}" was added successfully.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_add(request, obj)  

   
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre','autor', 'establecimiento')
    search_fields = ('nombre','autor', 'establecimiento')
    
admin.site.register(Grupo,GrupoAdmin)
admin.site.register(Encargado,EncargadoAdmin)
