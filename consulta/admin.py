from django.contrib import admin
from .models import Consulta, ConsultaPropuesta, ConsultaRespuesta

# Register your models here.

admin.site.register(Consulta)
admin.site.register(ConsultaPropuesta)
admin.site.register(ConsultaRespuesta)