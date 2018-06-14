from django.contrib import admin
from .models import Usuario
from django.contrib.auth.models import Group
# from social_django.models import Association, Nonce, UserSocialAuth


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email')
    #list_filter = ('created', 'updated', 'status')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email')
    fieldsets = [
        ('Banear usuario', {'fields': ['is_active']}),
    ]
admin.site.register(Usuario, UsuarioAdmin)

#oculta estos modelos
admin.site.unregister(Group)

# admin.site.unregister(Association)
# admin.site.unregister(Nonce)
# admin.site.unregister(UserSocialAuth)

