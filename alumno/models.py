from django.db import models
from administrador.models import Carrera, Genero, Track, TrackRequest
from login.models import User
from django.conf import settings
# Create your models here.


class Perfil_alumno(models.Model):
    alumno = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil_alumno', db_column='username')
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.ForeignKey(
        Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    genero = models.ForeignKey(
        Genero, on_delete=models.SET_NULL, blank=True, null=True)
    track_interes = models.ForeignKey(
        Track, on_delete=models.SET_NULL, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    imagen_perfil = models.ImageField(
        upload_to='images/', blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.alumno}'


class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nom_proyecto = models.CharField(max_length=50)
    jefe_proyecto = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='id_alumno')
    descripcion = models.CharField(max_length=250)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    imagen = models.ImageField(upload_to='images/')  # Quizas opcional
    objetivo = models.CharField(max_length=200)
    num_integrantes = models.IntegerField()
    id_track = models.ForeignKey(Track, models.CASCADE, db_column='idTrack')

    def __str__(self):
        return f'ID proyecto {self.id_proyecto}, Nombre proyecto: {self.nom_proyecto}'

    def jefe_usuario(self):
        return self.jefe_proyecto.alumno


class ProyectoRequest(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    id_solicitud = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name='solicitudes')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=10, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno} → {self.proyecto} ({self.estado})"


class Solicitud(models.Model):
    CATEGORIAS = [
        ('recurso', 'Recurso'),
        ('software', 'Mejora de Software'),
        ('logistica', 'Logística'),
        ('otro', 'Otro'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('resuelta', 'Resuelta'),
        ('rechazada', 'Rechazada'),
    ]

    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=20, choices=CATEGORIAS, default='otro')
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.alumno.username}'

class ProyectoPost(models.Model):
    id_post = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='posts')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.autor.username} en {self.proyecto.nom_proyecto}"

class ReunionProyecto(models.Model):
    id_reunion = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='reuniones')
    titulo = models.CharField(max_length=100, default='Reunión de Proyecto')
    fecha = models.DateField()
    hora = models.TimeField()
    modalidad = models.CharField(max_length=20, choices=[('presencial', 'Presencial'), ('virtual', 'Virtual')], default='presencial')
    link_virtual = models.URLField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reunión de {self.proyecto.nom_proyecto} el {self.fecha} a las {self.hora}"

class IntegranteProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='integrantes')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('proyecto', 'alumno')

    def __str__(self):
        return f"{self.alumno.username} en {self.proyecto.nom_proyecto}"
