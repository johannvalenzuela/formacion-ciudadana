from django.contrib import admin
from .models import Supervisor

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('usuario','asignatura', 'departamento_Provincial_Educacion', 'servicio_Local_Educacion')
    search_fields = ('usuario','asignatura', 'departamento_Provincial_Educacion', 'servicio_Local_Educacion')
admin.site.register(Supervisor,SupervisorAdmin)