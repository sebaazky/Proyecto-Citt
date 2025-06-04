from django.contrib import admin
from .models import PerfilDocente, Evento, DocentePost
# Register your models here.

admin.site.register(PerfilDocente)
admin.site.register(Evento)
admin.site.register(DocentePost)