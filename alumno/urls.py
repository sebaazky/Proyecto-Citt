from django.urls import path
from . import views
from .views import detalle_track_view

urlpatterns = [
    # Home
    path('home/', views.home_view, name='home-alumno'),
    # Reuniones
    path('reuniones/', views.reuniones_alumno_view, name='reuniones-alumno'),
    # Eventos
    path('eventos/', views.eventos_track_view, name='eventos-alumno'),
    # Perfil
    path('perfil/ver/', views.ver_perfil, name='ver-perfil-al'),
    path('perfil/', views.editar_perfil, name="edit-perfil-al"),
    # Gestión proyectos
    path('misproyectos/', views.listar_proyectos, name='listar-proyectos'),
    path('misproyectos/añadir/', views.añadir_proyecto, name='añadir-proyecto'),
    path('misproyectos/modificar/<int:pk>/', views.modificar_proyecto, name='modificar-proyecto'),
    # Tracks
    path('tracks/<int:track_id>/unirse/',
         views.unirse_a_track, name='unirse_a_track'),
    path('tracks/<int:track_id>/proyectos',
         views.lista_proyectos_citt, name='listar-proyectos-track'),
    path('tracks/proyectos/solicitar/<int:id_proyecto>/',
         views.solicitar_ingreso_proyecto, name='solicitar-ingreso-proyecto'),
    path('tracks/<slug:slug>/', views.detalle_track_view, name='detalle-track'),
    path('tracks/', views.listar_tracks, name='listar-tracks'),

    #Solicitudes Citt
    path('solicitudes/', views.listar_solicitudes_citt, name='listar-solicitudes'),
    path('solicitudes/crear/', views.crear_solicitud_citt, name='crear-solicitud'),
    path('solicitudes/modificar/<int:pk>/', views.modificar_solicitud_citt, name='modificar-solicitud'),
    # Flujo onboarding para alumnos nuevos
    path('onboarding/', views.flujo_onboarding, name='flujo-onboarding'),
    # Gestión de proyectos, solicitudes de ingreso al proyecto y post en mis proyectos.
    path('proyectos/<int:proyecto_id>/', views.home_proyecto_view, name='home-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/post/crear/', views.crear_post_proyecto, name='crear-post-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/reunion/crear/', views.crear_reunion_proyecto, name='crear-reunion-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/solicitar/', views.solicitar_ingreso_proyecto, name='solicitar-ingreso-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/solicitudes/', views.gestionar_solicitudes_proyecto, name='gestionar-solicitudes-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/solicitudes/<int:solicitud_id>/aceptar/', views.aceptar_solicitud_proyecto, name='aceptar-solicitud-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/solicitudes/<int:solicitud_id>/rechazar/', views.rechazar_solicitud_proyecto, name='rechazar-solicitud-proyecto-alumno'),
    path('proyectos/<int:id_proyecto>/cancelar-solicitud/', views.cancelar_solicitud_proyecto, name='cancelar-solicitud-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/post/<int:post_id>/modificar/', views.modificar_post_proyecto, name='modificar-post-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/post/<int:post_id>/eliminar/', views.eliminar_post_proyecto, name='eliminar-post-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/reunion/<int:reunion_id>/modificar/', views.modificar_reunion_proyecto_alumno, name='modificar-reunion-proyecto-alumno'),
    path('proyectos/<int:proyecto_id>/reunion/<int:reunion_id>/eliminar/', views.eliminar_reunion_proyecto_alumno, name='eliminar-reunion-proyecto-alumno'),
]
