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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar opción nula en carrera y genero
        if 'carrera' in self.fields:
            self.fields['carrera'].empty_label = None
        if 'genero' in self.fields:
            self.fields['genero'].empty_label = None

    class Meta:
        model = PerfilDocente
        exclude = ['usuario','docente']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['id_tipo_evento', 'nombre_evento',
                  'ubicacion_evento', 'fecha_evento', 'hora', 'infografia']
        widgets = {
            'id_tipo_evento': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'nombre_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 50,
                'pattern': r'^(?![0-9]+$)[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{1,50}$',
                'required': True
            }),
            'ubicacion_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'pattern': r'^(?![0-9]+$)[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.\-]{1,100}$',
                'required': True
            }),
            'fecha_evento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'min': '08:00', 'max': '23:00', 'required': True}),
            'infografia': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_nombre_evento(self):
        nombre = self.cleaned_data.get('nombre_evento', '')
        import re
        if not re.match(r'^(?![0-9]+$)[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{1,50}$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras, números y espacios, y no puede ser solo números.')
        return nombre

    def clean_ubicacion_evento(self):
        ubicacion = self.cleaned_data.get('ubicacion_evento', '')
        import re
        if not re.match(r'^(?![0-9]+$)[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.\-]{1,100}$', ubicacion):
            raise forms.ValidationError('La ubicación solo puede contener letras, números, espacios y ,.- y no puede ser solo números.')
        return ubicacion

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha_evento')
        hora = cleaned_data.get('hora')
        if fecha is None:
            self.add_error('fecha_evento', 'La fecha es obligatoria.')
        if hora is None:
            self.add_error('hora', 'La hora es obligatoria.')
        return cleaned_data


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
