from django.urls import path, include
from . import views

urlpatterns = [
    path('alumnos/', views.ListaAlumnosView.as_view(), name='alumnos'),
    path('apoderados/', views.ListaApoderadosView.as_view(), name='apoderados'),
    path('grupos/', views.ListaGruposView.as_view(), name='grupos'),
]