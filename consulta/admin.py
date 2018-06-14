from django.contrib import admin
from .models import Consulta, Consulta_propuesta, Consulta_respuesta

# Register your models here.

admin.site.register(Consulta)
admin.site.register(Consulta_propuesta)
admin.site.register(Consulta_respuesta)