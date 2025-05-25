from django import forms
from .models import Perfil_docente


class PerfilDocenteForm(forms.ModelForm):
    class Meta:
        model = Perfil_docente
        fields = ['p_nombre', 's_nombre', 'apellido_pat', 'apellido_mat',
                  'fecha_nacimiento', 'genero', 'telefono', 'imagen']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
