from django import forms
from .models import PerfilDocente, Evento, TrackPost, ReunionProyectoDocente
from administrador.models import ReunionTrack
from alumno.models import Proyecto, ProyectoPost


class ProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nom_proyecto', 'descripcion', 'imagen', 'objetivo',
                  'fecha_inicio', 'num_integrantes']  # id_track y jefe_proyecto se asignan en la vista

        widgets = {
            'nom_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'num_integrantes': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PerfilDocenteForm(forms.ModelForm):  # <-- este nombre sí coincide
    class Meta:
        model = PerfilDocente
        exclude = ['usuario','docente']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['id_tipo_evento', 'nombre_evento',
                  'ubicacion_evento', 'fecha_evento', 'hora', 'infografia']
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }


class ReunionTrackForm(forms.ModelForm):
    class Meta:
        model = ReunionTrack
        fields = ['track', 'fecha', 'hora', 'modalidad',
                  'link_virtual', 'ubicacion', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }


class DocentePostForm(forms.ModelForm):
    class Meta:
        model = TrackPost
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuerpo o descripción'}),
        }


class PostProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = ProyectoPost
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuerpo o descripción'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReunionProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = ReunionProyectoDocente
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
