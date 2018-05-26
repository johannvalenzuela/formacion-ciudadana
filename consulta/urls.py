from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.VisualizarConsultasView.as_view(), name='visualizar_consultas'),
]