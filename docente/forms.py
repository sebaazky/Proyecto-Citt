from django import forms
from .models import PerfilDocente, Evento

class PerfilFormDocente(forms.ModelForm):
    class Meta:
        model = PerfilDocente
        exclude = ['usuario']
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['id_tipo_evento', 'nombre_evento', 'ubicacion_evento', 'fecha_evento', 'hora', 'infografia']
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }