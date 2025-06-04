from django.urls import path
from . import views

urlpatterns = [
     path('home/', views.home_docente, name='home-docente'),
<<<<<<< Updated upstream
     path('perfil/', views.editar_perfil_docente, name="edit-perfil-docente"),
     path('solicitudes/', views.solicitudes_pendientes_view, name='solicitudes_pendientes'),
     path('solicitud/<int:solicitud_id>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
     path('solicitud/<int:solicitud_id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
     path('eventos/', views.listar_eventos, name='listar-eventos'),
     path('eventos/añadir/', views.añadir_evento, name='añadir-evento'),
     path('eventos/modificar/<int:pk>/', views.modificar_evento, name='modificar-evento'),
     path('eventos/eliminar/<int:pk>/', views.eliminar_evento, name='eliminar-evento'),
     path('mi-track/', views.mi_track_view, name='mi-track'),
     path('mi-track/post/crear/', views.crear_post_docente, name='crear-post-docente'),
     path('mi-track/post/<int:post_id>/eliminar/', views.eliminar_post_docente, name='eliminar-post-docente'),
     path('mi-track/post/<int:post_id>/modificar/', views.modificar_post_docente, name='modificar-post-docente'),
     path('mi-track/alumnos/', views.listado_alumnos_track, name='listado-alumnos-track'),
     path('mi-track/alumnos/eliminar/<int:alumno_id>/', views.eliminar_alumno_track, name='eliminar-alumno-track'),
     path('mi-track/solicitudes/', views.listado_solicitudes_track, name='listado-solicitudes-track'),
     path('mi-track/eventos/', views.listado_eventos_track, name='listado-eventos-track'),
     path('mi-track/reunion/<int:reunion_id>/', views.detalle_reunion_track, name='detalle-reunion-track'),
     path('mi-track/reunion/crear/', views.crear_reunion_track, name='crear-reunion-track'),
=======
     path('reuniones/', views.administrar_reuniones, name='administrar_reuniones'),
     path('proyectos/', views.administrar_proyectos, name='administrar_proyectos'),
     path('eventos/', views.administrar_eventos, name='administrar_eventos'),
     path('solicitudes/', views.administrar_solicitudes,
          name='administrar_solicitudes'),
     path('reportes/', views.generar_reportes, name='generar_reportes'),
     path('notificaciones/', views.enviar_notificaciones,
          name='enviar_notificaciones'),
     path('perfil/registrar/', views.registrar_perfil,
          name='registrar_perfil_docente'),
     path('track/<int:track_id>/solicitudes/', views.solicitudes_track_docente, name='solicitudes_track_docente'),





>>>>>>> Stashed changes
]
