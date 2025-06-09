from django import forms
from .models import PerfilDocente, Evento
from administrador.models import ReunionTrack
from alumno.models import Proyecto


class ProyectoDocenteForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
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
