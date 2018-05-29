
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from autenticacion.decorators import funcionario_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('autenticacion/', include('autenticacion.urls')),
    
    path('biblioteca_digital/', funcionario_required(include('biblioteca_digital.urls'))),
]
