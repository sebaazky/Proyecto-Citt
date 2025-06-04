from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home-alumno'),
    path('perfil/', views.editar_perfil, name="edit-perfil-al"),
    path('misproyectos/',views.listar_proyectos,name='listar-proyectos'),
    path('misproyectos/añadir/',views.añadir_proyecto,name='añadir-proyecto'),
    path('misproyectos/modificar/<int:pk>',views.modificar_proyecto,name='modificar-proyecto'),
    path('misproyectos/eliminar/<int:pk>',views.eliminar_proyecto,name='eliminar-proyecto'),
    path('tracks/robotica/', views.robotica_view, name='track-robotica'),
    path('tracks/ciberseguridad/', views.ciberseguridad_view, name='track-ciberseguridad'),
<<<<<<< Updated upstream
    path('tracks/bigdata/', views.bigdata_view, name='track-bigdata'),
    path('tracks/videojuegos/', views.videojuegos_view, name='track-videojuegos'),
    path('tracks/machinelearning/', views.machinelearning_view, name='track-machinelearning'),
    path('tracks/realidadvirtual/', views.realidadvirtual_view, name='track-realidadvirtual'),
    path('tracks/appmovilweb/', views.appmovilweb_view, name='track-appmovilweb'),
    path('tracks/iot/', views.iot_view, name='track-iot'),
    path('tracks/drones/', views.drones_view, name='track-drones'),
    path('tracks/<int:track_id>/unirse/', views.unirse_a_track, name='unirse_a_track'),
    path('misproyectos/error/', views.error_view, name='error-view'),
    path('tracks/<int:track_id>/proyectos', views.lista_proyectos_citt, name='listar-proyectos-track'),
    path('proyectos/solicitudes/', views.gestionar_solicitudes_proyecto, name='gestionar-solicitudes-proyecto'),
    path('tracks/proyectos/solicitar/<int:id_proyecto>/', views.solicitar_ingreso_proyecto, name='solicitar-ingreso-proyecto'),
=======
>>>>>>> Stashed changes
]