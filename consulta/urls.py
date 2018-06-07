from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.VisualizarConsultasView.as_view(), name='visualizar_consultas'),
    path('detallesconsulta/', views.DetallesConsultaView.as_view(), name='detalles_consulta'),
    path('crearconsulta/', views.CrearConsultaView.as_view(), name = 'crear_consulta'),
    path('detallesconsulta/crearpropuestaconsulta/', views.ConsultaCrearPropuestaView.as_view(), name ='crear_propuesta'),
    path('detallesconsulta/responderconsulta/', views.ResponderConsultaView.as_view(), name= 'responder_consulta'),
    path('visualizarpropuestaconsulta/', views.ConsultaVisualizarPropuestaView.as_view(), name= 'propuesta_consulta'),
]
