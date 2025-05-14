from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('alumnos/', include('alumno.urls')),
    path('login/', include('login.urls')),
    path('docente/', include('docente.urls')),
    ]

