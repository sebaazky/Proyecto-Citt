from django import forms
from alumno.models import Perfil_alumno, Proyecto

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil_alumno
        exclude = ['usuario']

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nom_proyecto', 'jefe_proyecto', 'descripcion', 'fecha_inicio', 'imagen', 'objetivo', 'num_integrantes', 'id_track']
