from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username", max_length=150)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

class RegistroAlumnoForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']