
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_iipj/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('autenticacion/', include('autenticacion.urls')),
    path('biblioteca_digital/', include('biblioteca_digital.urls')),
    path('gestion_usuarios/', include('gestion_usuarios.urls')),
    path('consulta/', include('consulta.urls')),
    path('analitica', include('analitica.urls')),
]
if  settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)