from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('proyectos/',views.proyectos,name='proyectos'),
    path('track/',views.track,name='track'),
]