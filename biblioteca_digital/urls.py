from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from autenticacion.decorators import funcionario_required


urlpatterns = [
    path('', views.BibliotecaView.as_view(), name='biblioteca_digital'),
    path('<pk>/', views.RecursoDetailView.as_view(), name='recurso-detail'),
    path('<pk>/editar', views.RecursoUpdateView.as_view(), name='recurso-update'),
    path('<pk>/valorar/', views.RecursoDetailView.valorar, name='valorar'), 
    path('<pk>/descargar/', views.descargar, name= 'descargar'),
    path('recurso_nuevo/', views.CrearRecursoView.as_view(), name='recurso_nuevo'),
]

if  settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)