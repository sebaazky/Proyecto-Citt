from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.admin_home, name='admin-home'),
    path('reporte-pdf/', views.admin_reporte_pdf, name='admin-reporte-pdf'),
    path('enviar-correos/', views.admin_enviar_correos,
         name='admin-enviar-correos'),

    path('admin/perfil/', views.ver_perfil_administrador, name='ver-perfil-admin'),
    path('admin/perfil/modificar/', views.modificar_perfil_admin,
         name='modificar-perfil-admin'),

    path('gestion-proyectos/', views.listar_proyectos,
         name='admin-gestion-proyectos'),
    path('crear-proyecto/', views.crear_proyecto,
         name='admin-crear-proyecto'),
    path('modificar-proyecto/<int:id_proyecto>/',
         views.modificar_proyecto, name='admin-modificar-proyecto'),
    path('eliminar-proyecto/<int:id_proyecto>/',
         views.eliminar_proyecto, name='admin-eliminar-proyecto'),

    path('gestion-solicitudes/', views.listar_solicitudes,
         name='admin-gestion-solicitudes'),
    path('modificar-solicitud/<int:solicitud_id>/',
         views.modificar_solicitud, name='admin-modificar-solicitud'),
    path('eliminar-solicitud/<int:solicitud_id>/',
         views.eliminar_solicitud, name='admin-eliminar-solicitud'),

    path('gestion-eventos/', views.listar_eventos, name='admin-gestion-eventos'),
    path('crear-evento/', views.crear_evento, name='admin-crear-evento'),
    path('modificar-evento/<int:id_evento>/',
         views.modificar_evento, name='admin-modificar-evento'),
    path('eliminar-evento/<int:id_evento>/',
         views.eliminar_evento, name='admin-eliminar-evento'),

    path('admin/docentes/', views.admin_listar_docentes,
         name='admin-gestion-docentes'),
    path('admin/docentes/crear/', views.admin_crear_perfil_docente,
         name='admin-crear-docente'),
    path('admin/docentes/modificar/<int:pk>/',
         views.admin_modificar_docente, name='admin-modificar-docente'),
    path('admin/docentes/eliminar/<int:pk>/',
         views.admin_eliminar_docente, name='admin-eliminar-docente'),

    path('admin/alumnos/', views.admin_listar_alumnos,
         name='admin-gestion-alumnos'),
    path('admin/alumnos/crear/', views.admin_crear_alumno,
         name='admin-crear-alumno'),
    path('admin/alumnos/modificar/<int:pk>/',
         views.admin_modificar_alumno, name='admin-modificar-alumno'),
    path('admin/alumnos/eliminar/<int:pk>/',
         views.admin_eliminar_alumno, name='admin-eliminar-alumno'),


    path('admin/usuarios/', views.admin_listar_usuarios,
         name='admin-gestion-usuarios'),
    path('admin/usuarios/crear/', views.admin_crear_usuario,
         name='admin-crear-usuario'),
    path('admin/usuarios/modificar/<int:pk>/',
         views.admin_modificar_usuario, name='admin-modificar-usuario'),
    path('admin/usuarios/eliminar/<int:pk>/',
         views.admin_eliminar_usuario, name='admin-eliminar-usuario'),



    path('admin/tracks/', views.listar_tracks, name='admin-listar-tracks'),
    path('admin/tracks/crear/', views.crear_track, name='admin-crear-track'),
    path('admin/tracks/modificar/<int:id_track>/',
         views.modificar_track, name='admin-modificar-track'),
    path('admin/tracks/eliminar/<int:id_track>/',
         views.eliminar_track, name='admin-eliminar-track'),

]
