from django import forms
from .models import PerfilAdministrador

class PerfilAdministradorForm(forms.ModelForm):
    class Meta:
        model = PerfilAdministrador
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'imagen_perfil']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
