from django.urls import path, include
from . import views

urlpatterns = [
    path('lista_usuarios/<str:nombreGrupo>/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('grupos/', views.ListaGruposView.as_view(), name='lista_grupos'),
    path('agregar_usuario_form/<int:pk_grupo>', views.agregarUsuarioFormView, name='agregar_usuario_form'),
    path('agregar_usuario_grupo/<int:pk_grupo>', views.agregarUsuario, name='agregar_usuario'),
    path('remover_usuario_grupo_form/<int:pk_grupo>/<int:pk_usuario>', views.removerUsuarioView, name='remover_usuario_form'),
    path('remover_usuario_grupo/<int:pk_grupo>/<int:pk_usuario>', views.removerUsuario, name='remover_usuario'),
]