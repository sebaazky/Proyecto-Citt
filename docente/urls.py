from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('home/', views.home_docente, name='home-docente'),
    # Perfil
    path('perfil/ver/', views.ver_perfil_docente, name='ver-perfil-doc'),
    path('perfil/editar/', views.editar_perfil_docente, name='edit-perfil-doc'),
    # Gestion de solicitudes de ingreso a mi track
    path('solicitudes/', views.solicitudes_pendientes_view,
         name='solicitudes_pendientes'),
    path('solicitud/<int:solicitud_id>/aprobar/',
         views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/',
         views.rechazar_solicitud, name='rechazar_solicitud'),
     # Gestión de eventos
    path('eventos/', views.listar_eventos, name='listar-eventos'),
    path('eventos/añadir/', views.añadir_evento, name='añadir-evento'),
    path('eventos/modificar/<int:pk>/',
         views.modificar_evento, name='modificar-evento'),
    path('eventos/eliminar/<int:pk>/',
         views.eliminar_evento, name='eliminar-evento'),
     # Track del docente, gestion de post y solicitudes de ingreso al track
    path('mi-track/', views.mi_track_view, name='mi-track'),
    path('mi-track/post/crear/', views.crear_post_docente,
         name='crear-post-track-docente'),
    path('mi-track/post/<int:post_id>/eliminar/',
         views.eliminar_post_docente, name='eliminar-post-track-docente'),
    path('mi-track/post/<int:post_id>/modificar/',
         views.modificar_post_docente, name='modificar-post-track-docente'),

    path('mi-track/alumnos/', views.listado_alumnos_track,
         name='listado-alumnos-track'),
    path('mi-track/alumnos/eliminar/<int:alumno_id>/',
         views.eliminar_alumno_track, name='eliminar-alumno-track'),
    path('mi-track/solicitudes/', views.listado_solicitudes_track,
         name='listado-solicitudes-track'),

    path('mi-track/eventos/', views.listado_eventos_track,
         name='listado-eventos-track'),

    path('mi-track/reuniones/', views.listar_reuniones_track,
         name='listar-reuniones-track'),
    path('mi-track/reuniones/crear/',
         views.crear_reunion_track, name='crear-reunion-track'),
    path('mi-track/reuniones/<int:pk>/editar/',
         views.editar_reunion_track, name='editar-reunion-track'),
    path('mi-track/reuniones/<int:pk>/eliminar/',
         views.eliminar_reunion_track, name='eliminar-reunion-track'),
    path('mi-track/reuniones/<int:pk>/detalle/',
         views.detalle_reunion_modal, name='detalle-reunion-track'),

     # Gestión de mis proyectos
    path('proyectos/', views.listar_proyectos_docente,
         name='listar-proyectos-docente'),
    path('proyectos/crear/', views.crear_proyecto_docente,
         name='crear-proyecto-docente'),
    path('proyectos/modificar/<int:pk>/', views.modificar_proyecto_docente,
         name='modificar-proyecto-docente'),
    path('proyectos/eliminar/<int:pk>/', views.eliminar_proyecto_docente,
         name='eliminar-proyecto-docente'),

    path('proyectos/<int:proyecto_id>/', views.home_proyecto_docente, name='home-proyecto-docente'),

    path('proyectos/<int:proyecto_id>/post/crear/', views.crear_post_proyecto_docente, name='crear-post-proyecto-docente'),
    path('proyectos/<int:proyecto_id>/post/<int:post_id>/modificar/', views.modificar_post_proyecto_docente, name='modificar-post-proyecto-docente'),
    path('proyectos/<int:proyecto_id>/post/<int:post_id>/eliminar/', views.eliminar_post_proyecto_docente, name='eliminar-post-proyecto-docente'),

    path('proyectos/<int:proyecto_id>/reunion/crear/', views.crear_reunion_proyecto_docente, name='crear-reunion-proyecto-docente'),
    path('proyectos/<int:proyecto_id>/reunion/<int:reunion_id>/modificar/', views.modificar_reunion_proyecto_docente, name='modificar-reunion-proyecto-docente'),
    path('proyectos/<int:proyecto_id>/reunion/<int:reunion_id>/eliminar/', views.eliminar_reunion_proyecto_docente, name='eliminar-reunion-proyecto-docente'),

]
