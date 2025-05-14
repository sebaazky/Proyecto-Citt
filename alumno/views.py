from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido

@login_required
@rol_requerido('alumno')
def home_view(request):
    return render(request, 'home_alumno.html')
