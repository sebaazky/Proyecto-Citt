from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='login-alumno'),
    path('registro/', views.registrar_alumno, name='registro-alumno'),
    path('logout/', views.logout_view, name='logout'),
]