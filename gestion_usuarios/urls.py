from django.urls import path, include
from . import views

urlpatterns = [
    path('lista_usuarios/<str:nombreGrupo>/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('grupos/', views.ListaGruposView.as_view(), name='lista_grupos'),
    path('grupos/agregar_grupo/', views.AgregarGrupoView.as_view(), name='agregar_grupo'),
    path('grupos/eliminar_grupo/<int:pk>/', views.EliminarGrupoView.as_view(), name='eliminar_grupo'),
    path('grupos/editar_grupo/<int:pk>/', views.EditarGrupoView.as_view(), name='editar_grupo'),
    path('agregar_usuario_form/<int:pk_grupo>', views.AgregarUsuarioGrupoView.as_view(), name='agregar_usuario_form'),
    path('remover_usuario_grupo_form/<int:pk_grupo>/<int:pk_usuario>', views.EliminarUsuarioGrupoView.as_view(), name='remover_usuario_form'),
    #Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/editar', views.ProfileUpdateView.as_view(), name='profile_editar'),
]