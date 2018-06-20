from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ActividadesListView.as_view() ,name='visualizar_actividades'),
]