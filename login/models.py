from django.contrib.auth.models import AbstractUser
from django.db import models
from administrador.models import Track


class User(AbstractUser):
    ROLES = [
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
        ('administrador', 'Administrador'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    id_track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
