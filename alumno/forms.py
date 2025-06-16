from django import forms
from alumno.models import Perfil_alumno, Proyecto, Solicitud
from .models import ProyectoPost, ReunionProyecto


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil_alumno
        exclude = ['alumno', 'track_interes']  # Eliminamos estos campos

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nom_proyecto', 'descripcion', 'imagen',
                  'objetivo', 'num_integrantes']

        widgets = {
            'nom_proyecto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe brevemente tu proyecto'
            }),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'objetivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objetivo del proyecto'
            }),
            'num_integrantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad de integrantes'
            }),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo', 'descripcion', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class ProyectoPostForm(forms.ModelForm):
    class Meta:
        model = ProyectoPost
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Qué quieres compartir?'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReunionProyectoForm(forms.ModelForm):
    class Meta:
        model = ReunionProyecto
        fields = ['titulo', 'fecha', 'hora', 'modalidad', 'link_virtual', 'ubicacion', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'link_virtual': forms.URLInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

