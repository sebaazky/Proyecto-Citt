from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home-alumno'),
    # path('home-docente/', views.home_docente_view, name='home-docente'),
]