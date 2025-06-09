from django.urls import path
from . import views
from .views import detalle_track_view

urlpatterns = [
    path('home/', views.home_view, name='home-alumno'),

    path('perfil/ver/', views.ver_perfil, name='ver-perfil-al'),
    path('perfil/', views.editar_perfil, name="edit-perfil-al"),

    # Gestión de proyectos
    path('misproyectos/', views.listar_proyectos, name='listar-proyectos'),
    path('misproyectos/añadir/', views.añadir_proyecto, name='añadir-proyecto'),
    path('misproyectos/modificar/<int:pk>/',
         views.modificar_proyecto, name='modificar-proyecto'),

    # Track y proyectos CITT
    path('tracks/<int:track_id>/unirse/',
         views.unirse_a_track, name='unirse_a_track'),
    path('tracks/<int:track_id>/proyectos',
         views.lista_proyectos_citt, name='listar-proyectos-track'),
    path('proyectos/solicitudes/', views.gestionar_solicitudes_proyecto,
         name='gestionar-solicitudes-proyecto'),
    path('tracks/proyectos/solicitar/<int:id_proyecto>/',
         views.solicitar_ingreso_proyecto, name='solicitar-ingreso-proyecto'),

    # Detalle dinámico del track
    path('tracks/<slug:slug>/', detalle_track_view, name='detalle-track'),


    path('reuniones/', views.reuniones_alumno_view, name='reuniones-alumno'),

    path('eventos/', views.eventos_track_view, name='eventos-alumno'),

    path('solicitudes/', views.listar_solicitudes, name='listar-solicitudes'),
    path('solicitudes/crear/', views.crear_solicitud, name='crear-solicitud'),
    path('solicitudes/modificar/<int:pk>/',
         views.modificar_solicitud, name='modificar-solicitud'),


]
