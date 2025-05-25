from django.db import models


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True, db_column='idGenero')
    nom_genero = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nom_genero)


class Perfil_docente(models.Model):
    id_docente = models.AutoField(primary_key=True, db_column='idDocente')
    p_nombre = models.CharField(max_length=15)
    s_nombre = models.CharField(max_length=15)
    apellido_pat = models.CharField(max_length=15)
    apellido_mat = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(null=False)
    genero = models.ForeignKey(
        Genero, on_delete=models.CASCADE, db_column='idGenero')
    telefono = models.IntegerField()
    imagen = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'ID alumno {self.id_docente}, Nombre: {self.p_nombre} {self.apellido_pat}'
