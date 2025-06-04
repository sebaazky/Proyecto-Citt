from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'id': 'usuario',
            'class': 'form-control form-control-sm',
            'placeholder': 'Usuario',
            'required': True,
        })
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={
            'id': 'password1',
            'class': 'form-control form-control-sm',
            'placeholder': 'Contraseña',
            'required': True,
        })
    )

class RegistroAlumnoForm(UserCreationForm):
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Usuario',
            'required': True,
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Contraseña',
            'required': True,
        })
    )
    password2 = forms.CharField(
        label="Repite la contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Repite la contraseña',
            'required': True,
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data