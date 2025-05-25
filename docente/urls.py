from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_docente, name='home-docente'),
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





]
