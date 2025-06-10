from django import forms
from alumno.models import Perfil_alumno, Proyecto, Solicitud


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
                  'objetivo', 'num_integrantes', 'id_track']

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
            # <- agregado
            'id_track': forms.Select(attrs={'class': 'form-control'})
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo', 'descripcion', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
