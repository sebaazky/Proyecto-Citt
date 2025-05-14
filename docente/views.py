from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido

# Create your views here.

@login_required
@rol_requerido('docente')
def home_docente(request):
    return render(request, 'home-docente.html')