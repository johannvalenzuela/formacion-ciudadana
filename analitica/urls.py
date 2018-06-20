from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ActividadesListView.as_view() ,name='visualizar_actividades'),
    path('lista_actividades/agregar_supervisor', views.AsociarEncargadoView.as_view() ,name='agregar_supervisor'),
]