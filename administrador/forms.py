from django import forms
from .models import PerfilAdministrador
from alumno.models import Proyecto, Solicitud
from docente.models import Evento, PerfilDocente
from login.models import User
from alumno.models import Perfil_alumno
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from administrador.models import Track
from django.db import models


class PerfilAdministradorForm(forms.ModelForm):
    class Meta:
        model = PerfilAdministrador
        fields = ['nombres', 'apellido_paterno',
                  'apellido_materno', 'genero', 'imagen_perfil']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),


        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['alumno', 'titulo', 'descripcion', 'categoria', 'estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }


class PerfilDocenteForm(forms.ModelForm):
    class Meta:
        model = PerfilDocente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['docente'].disabled = True


class CrearPerfilDocenteForm(forms.ModelForm):
    class Meta:
        model = PerfilDocente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo usuarios con rol 'docente' que no tienen perfil ya creado
        self.fields['docente'].queryset = User.objects.filter(
            rol='docente'
        ).exclude(perfil_docente__isnull=False)


class CrearPerfilAlumnoForm(forms.ModelForm):
    class Meta:
        model = Perfil_alumno
        exclude = ['track_interes']  # no mostrar este campo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir usuarios con perfil ya creado
        self.fields['alumno'].queryset = User.objects.filter(
            rol='alumno').exclude(perfil_alumno__isnull=False)


class ModificarPerfilAlumnoForm(forms.ModelForm):
    class Meta:
        model = Perfil_alumno
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bloquear campo 'alumno' al modificar
        self.fields['alumno'].disabled = True


User = get_user_model()


class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'rol',
                  'id_track', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar clases Bootstrap
        for field_name in self.fields:
            if field_name in ['rol', 'id_track']:
                self.fields[field_name].widget.attrs.update(
                    {'class': 'form-select'})
            else:
                self.fields[field_name].widget.attrs.update(
                    {'class': 'form-control'})


class ModificarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'rol', 'id_track']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Desactiva el campo username (como ya lo tenías)
        self.fields['username'].disabled = True

        # Oculta el campo id_track si el usuario es administrador
        instance = kwargs.get('instance')
        if instance and instance.rol == 'administrador':
            self.fields['id_track'].widget = forms.HiddenInput()
            self.fields['id_track'].required = False


class CrearTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['nom_track', 'descripcion', 'imagen', 'id_usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo docentes sin track
        self.fields['id_usuario'].queryset = User.objects.filter(
            rol='docente', id_track__isnull=True
        )


class ModificarTrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['nom_track', 'descripcion', 'imagen', 'id_usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_usuario'].queryset = User.objects.filter(rol='docente')
