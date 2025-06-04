from django.db import models
from login.models import User
from administrador.models import Carrera, Genero, TipoEvento, Track

# Create your models here.

class PerfilDocente(models.Model):
    docente = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_docente', db_column='username')
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='images/', blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.docente.username}'
    
class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True, verbose_name='id_evento')
    docente = models.ForeignKey(User, on_delete=models.CASCADE, db_column='username')
    id_tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, db_column='idTipoEvento')
    nombre_evento = models.CharField(max_length=50)
    ubicacion_evento = models.CharField(max_length=100)
    fecha_evento = models.DateField(null=True)
    hora = models.TimeField(null=True)
    infografia = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'ID:{self.id_evento}-{self.nombre_evento}'

class DocentePost(models.Model):
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_docente', db_column='username')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='posts_track', db_column='idTrack')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'Post by {self.docente.username} on {self.fecha_creacion}'