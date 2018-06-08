from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email')
    #list_filter = ('created', 'updated', 'status')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email')
    fieldsets = [
        ('Banear usuario', {'fields': ['is_active']}),
    ]


admin.site.register(Usuario, UsuarioAdmin)

