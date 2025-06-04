from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Carrera)
admin.site.register(Genero)
admin.site.register(Comuna)
admin.site.register(Track)
admin.site.register(TrackRequest)
admin.site.register(TipoEvento)