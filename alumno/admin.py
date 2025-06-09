from django.contrib import admin
from .models import Perfil_alumno, Proyecto, ProyectoRequest

# Register your models here.

admin.site.register(Perfil_alumno)
admin.site.register(Proyecto)
admin.site.register(ProyectoRequest)
