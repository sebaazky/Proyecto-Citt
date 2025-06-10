from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.admin_home, name='admin-home'),
    path('reporte-pdf/', views.admin_reporte_pdf, name='admin-reporte-pdf'),
    path('enviar-correos/', views.admin_enviar_correos, name='admin-enviar-correos'),
    path('crear-docente/', views.admin_crear_docente, name='admin-crear-docente'),
    path('gestion-roles/', views.admin_gestion_roles, name='admin-gestion-roles'),
    path('gestion-usuarios/', views.admin_gestion_usuarios, name='admin-gestion-usuarios'),
    path('gestion-tracks/', views.admin_gestion_tracks, name='admin-gestion-tracks'),
    path('crear-usuario/', views.admin_crear_usuario, name='admin-crear-usuario'),
    path('eliminar-usuario/<int:user_id>/', views.admin_eliminar_usuario, name='admin-eliminar-usuario'),
    path('editar-track/<int:track_id>/', views.admin_editar_track, name='admin-editar-track'),
    path('agregar-track/', views.admin_agregar_track, name='admin-agregar-track'),
    path('perfil/', views.admin_perfil, name='admin-perfil'),
]
