from django.db import models
from login.models import User
# Create your models here.

# #Modelos en comun

# #Proyecto

# class Proyecto(models.Model):
#     id_proyecto = models.AutoField(primary_key=True)
#     nom_proyecto = models.CharField(max_length=50)
#     jefe_proyecto = models.ForeignKey(Perfil_alumno, on_delete=models.CASCADE,db_column='id_alumno')
#     descripcion = models.CharField(max_length=250)
#     fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
#     imagen = models.ImageField(upload_to='images/') #Quizas opcional
#     objetivo = models.CharField(max_length=200)
#     id_track = models.ForeignKey(Track,models.CASCADE,db_column='idTrack')
#     def __str__(self):
#         return f'ID proyecto {self.id_proyecto}, Nombre proyecto: {self.nom_proyecto}'

# #Reuniones

# class Reunion():
#     #id
#     #Nombre
#     #Fechayhora
#     #id_tiporeunion(foranea)
#     #id_usuario(foranea)
#     #descripcion
#     #Modalidad -- Lugar fisico o URL de la meet
#     #Lugar (opcional)
#     #Url (opcional)
#     #id_tiporeunion

# class Modalidad():
#     #id
#     #descripcion

# class TipoReunion():
#     #id
#     #nombre (track, citt, proyecto)
    
# #Notificaciones Por correo

# class NotificacionPorCorreo():
#     #id
#     #Asunto
#     #descripcion
#     #destinatario
#     #fecha

# # Eventos

# class Evento():
#     #id
#     #Nombre
#     #Ubicacion
#     #Imagen
#     #Datetime
#     #Tipoevento

# class TipoEvento():
#     #id
#     #nombre

# #Solicitudes generales

# class Solicitud():
#     #id
#     #nombre
#     #id_tipo
#     #id_usuario(foranea)
#     #descripcion
#     #imagen(opcional)

# class TipoSolitud():
#     #id
#     #nombre

# #Track

# class Track():
#     #id
#     #nombre
#     #id_docente(Foranea)
#     #Imagen
#     #Descripcion

# class Alumno_track():
#     #id_alumno
#     #id_track
#     #Datetime

