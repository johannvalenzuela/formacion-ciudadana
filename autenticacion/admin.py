from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'tipo')
    #list_filter = ('created', 'updated', 'status')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'tipo')
    fieldsets = [
        ('Cambiar tipo de usuario', {'fields': ['tipo']}),
        ('Banear usuario', {'fields': ['is_active']}),
    ]


admin.site.register(Usuario, UsuarioAdmin)

