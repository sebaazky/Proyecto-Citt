from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)