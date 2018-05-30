from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from autenticacion.decorators import funcionario_required


urlpatterns = [
    path('', funcionario_required(views.BibliotecaView.as_view())),
    path('<pk>/', funcionario_required(views.RecursoDetailView.as_view()), name='recurso-detail'),
    path('<pk>/valorar', funcionario_required(views.RecursoDetailView.valorar), name='valorar'), 
    path('<pk>/descargar/', funcionario_required(views.descargar), name= 'descargar'),
]

if  settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)