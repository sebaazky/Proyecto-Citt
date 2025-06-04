from django.db import models
from administrador.models import Carrera, Genero, Track
from login.models import User

# Create your models here.

class Perfil_alumno(models.Model):
    alumno = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_alumno', db_column='username')
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, blank=True, null=True)
    track_interes = models.ForeignKey(Track, on_delete=models.SET_NULL, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='images/', blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.alumno}'
    
class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nom_proyecto = models.CharField(max_length=50)
    jefe_proyecto = models.ForeignKey(Perfil_alumno, on_delete=models.CASCADE,db_column='id_alumno')
    descripcion = models.CharField(max_length=250)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    imagen = models.ImageField(upload_to='images/') #Quizas opcional
    objetivo = models.CharField(max_length=200)
    num_integrantes = models.IntegerField()
    id_track = models.ForeignKey(Track,models.CASCADE,db_column='idTrack')
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
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='solicitudes')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno.username} → {self.proyecto.nom_proyecto} ({self.estado})"