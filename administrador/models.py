from django.db import models
from django.conf import settings

# Create your models here.


class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True, db_column='idCarrera')
    nom_carrera = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nom_carrera)


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True, db_column='idGenero')
    nom_genero = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nom_genero)


class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True, db_column='idComuna')
    nom_comuna = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nom_comuna)


class TipoEvento(models.Model):
    id_tipo_evento = models.AutoField(
        primary_key=True, verbose_name='idTipoEvento')
    nombre_tipo_evento = models.CharField(max_length=25)

    def __str__(self):
        return str(self.nombre_tipo_evento)


class Track(models.Model):
    id_track = models.AutoField(primary_key=True, db_column='idTrack')
    nom_track = models.CharField(max_length=30)
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'docente'},
        db_column='idUsuario'
    )
    descripcion = models.CharField(
        max_length=250, default='Descripción del track')
    imagen = models.ImageField(
        upload_to='images/', default='images/default_track.png')

    def __str__(self):
        return str(self.nom_track)


class TrackRequest(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    id_solicitud = models.AutoField(primary_key=True, db_column='idSolicitud')
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='solicitudes')
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=10, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno} → {self.track} ({self.estado})"


class ReunionTrack(models.Model):
    id_reunion = models.AutoField(primary_key=True, db_column='idReunion')
    id_docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='idDocente')
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='reuniones')
    fecha = models.DateField()
    hora = models.TimeField()
    modalidad = models.CharField(max_length=20, choices=[(
        'presencial', 'Presencial'), ('virtual', 'Virtual')], default='presencial')
    link_virtual = models.URLField(
        blank=True, null=True, help_text="Enlace para reuniones virtuales")
    ubicacion = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return f"Reunión de {self.track.nom_track} el {self.fecha} a las {self.hora}"


class PerfilAdministrador(models.Model):
    from login.models import User
    from .models import Genero
    administrador = models.OneToOneField(
        'login.User', on_delete=models.CASCADE, related_name='perfil_administrador', db_column='username')
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    genero = models.ForeignKey(
        'Genero', on_delete=models.SET_NULL, blank=True, null=True)
    imagen_perfil = models.ImageField(
        upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'{self.administrador.username}'
