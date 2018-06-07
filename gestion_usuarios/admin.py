from django.contrib import admin
from .models import Servicio_Local_Educacion
from .models import Departamento_Provincial_Educacion
from .models import Establecimiento
from .models import Asignatura
from .models import Encargado


admin.site.register(Servicio_Local_Educacion)
admin.site.register(Departamento_Provincial_Educacion)
admin.site.register(Establecimiento)
admin.site.register(Asignatura)
admin.site.register(Encargado)