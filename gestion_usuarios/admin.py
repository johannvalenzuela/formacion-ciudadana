from django.contrib import admin
from .models import Servicio_Local_Educacion,Departamento_Provincial_Educacion,Establecimiento,Asignatura

admin.site.register(Servicio_Local_Educacion)
admin.site.register(Departamento_Provincial_Educacion)
admin.site.register(Establecimiento)
admin.site.register(Asignatura)

