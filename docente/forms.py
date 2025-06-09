from django import forms
from .models import PerfilDocente, Evento
from administrador.models import ReunionTrack
from alumno.models import Proyecto


class ProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nom_proyecto', 'descripcion', 'imagen', 'objetivo',
                  'fecha_inicio', 'num_integrantes', 'id_track', 'jefe_proyecto']

        widgets = {
            'nom_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'num_integrantes': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_track': forms.Select(attrs={'class': 'form-control'}),
            'jefe_proyecto': forms.Select(attrs={'class': 'form-control'}),
        }


class PerfilDocenteForm(forms.ModelForm):  # <-- este nombre sí coincide
    class Meta:
        model = PerfilDocente
        exclude = ['usuario']


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
