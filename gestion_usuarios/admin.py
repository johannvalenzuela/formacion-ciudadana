from django.contrib import admin
from .models import Servicio_Local_Educacion
from .models import Departamento_Provincial_Educacion
from .models import Establecimiento
from .models import Asignatura
from .models import Encargado
from .models import Supervisor


admin.site.register(Servicio_Local_Educacion)
admin.site.register(Departamento_Provincial_Educacion)
admin.site.register(Establecimiento)
admin.site.register(Asignatura)



class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('usuario','asignatura', 'establecimiento')
    search_fields = ('usuario','asignatura', 'establecimiento')

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('usuario','asignatura', 'departamento_Provincial_Educacion', 'servicio_Local_Educacion')
    search_fields = ('usuario','asignatura', 'departamento_Provincial_Educacion', 'servicio_Local_Educacion')
    

admin.site.register(Encargado,EncargadoAdmin)
admin.site.register(Supervisor,SupervisorAdmin)