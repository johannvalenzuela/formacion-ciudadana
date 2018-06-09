from django.urls import path, include
from . import views

urlpatterns = [
    path('lista_usuarios/<str:nombreGrupo>/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('grupos/', views.ListaGruposView.as_view(), name='lista_grupos'),
    path('<str:nombreGrupo>/agregar_usuario_grupo/<int:pk>/', views.agregarUsuario, name='agregar_usuario'),
    path('<str:nombreGrupo>/remover_usuario_grupo/<int:pk>/', views.removerUsuario, name='remover_usuario'),
]