from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido
from .forms import PerfilDocenteForm

# Create your views here.


@login_required
@rol_requerido('docente')
def home_docente(request):
    return render(request, 'home-docente.html')


def administrar_reuniones(request):
    return render(request, 'reunion/administrar_reuniones.html')


def administrar_proyectos(request):
    return render(request, 'proyecto/administrar_proyectos.html')


def administrar_eventos(request):
    return render(request, 'evento/administrar_eventos.html')


def administrar_solicitudes(request):
    return render(request, 'solicitud/administrar_solicitudes.html')


def generar_reportes(request):
    return render(request, 'reporte/generar_reportes.html')


def enviar_notificaciones(request):
    return render(request, 'notificacion/enviar_notificaciones.html')


def registrar_perfil(request):
    if request.method == 'POST':
        form = PerfilDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirige al home o a donde tú quieras
            return redirect('home-docente')
    else:
        form = PerfilDocenteForm()
    return render(request, 'docente/registrar_perfil.html', {'form': form})
