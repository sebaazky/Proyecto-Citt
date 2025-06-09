from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from login.decorators import rol_requerido
from .models import Perfil_alumno, Proyecto, ProyectoRequest, Solicitud
from .forms import PerfilForm, ProyectoForm, SolicitudForm
from administrador.models import Track, TrackRequest, ReunionTrack
from docente.models import DocentePost, Evento
from django.utils import timezone


# Home


@login_required
@rol_requerido('alumno')
def home_view(request):
    perfil = Perfil_alumno.objects.filter(alumno=request.user).first()
    context = {
        'perfil_alumno': perfil,
    }
    return render(request, 'home_alumno.html', context)

# Perfil


@login_required
@rol_requerido('alumno')
def ver_perfil(request):
    perfil = get_object_or_404(Perfil_alumno, alumno=request.user)
    return render(request, 'perfil/ver_perfil.html', {'perfil': perfil})


@login_required
@rol_requerido('alumno')
def editar_perfil(request):
    try:
        perfil = Perfil_alumno.objects.get(alumno=request.user)
    except Perfil_alumno.DoesNotExist:
        return redirect('perfil-alumno')

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home-alumno')
    else:
        form = PerfilForm(instance=perfil)

    context = {'form': form}
    return render(request, 'perfil/editar_perfil.html', context)

# Proyectos


@login_required
@rol_requerido('alumno')
def listar_proyectos(request):
    track_id = request.user.id_track
    proyectos = Proyecto.objects.filter(
        jefe_proyecto=request.user, id_track=track_id)
    context = {'proyectos': proyectos, 'track_id': track_id}
    return render(request, 'proyectos/listar_proyectos.html', context)


@login_required
@rol_requerido('alumno')
def añadir_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.jefe_proyecto = request.user  # ← Aquí
            proyecto.fecha_inicio = timezone.now().date()
            proyecto.save()
            return redirect('listar-proyectos')
    else:
        form = ProyectoForm()

    return render(request, 'proyectos/crear_proyecto.html', {'form': form})


@login_required
@rol_requerido('alumno')
def modificar_proyecto(request, pk):
    try:
        proyecto = Proyecto.objects.get(id_proyecto=pk)
        if request.method == 'POST':
            form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
            if form.is_valid():
                form.save()
                return redirect('listar-proyectos')
        else:
            form = ProyectoForm(instance=proyecto)
        context = {'form': form}
        return render(request, 'proyectos/modificar_proyecto.html', context)
    except Proyecto.DoesNotExist:
        return redirect('listar-proyectos')


# Unirse a track


@login_required
@rol_requerido('alumno')
def unirse_a_track(request, track_id):
    if request.method == 'POST':
        track = get_object_or_404(Track, id_track=track_id)
        if not TrackRequest.objects.filter(track=track, alumno=request.user, estado='pendiente').exists():
            TrackRequest.objects.create(track=track, alumno=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home-alumno'))

# Listar proyectos del track


@login_required
@rol_requerido('alumno')
def lista_proyectos_citt(request, track_id):
    track = get_object_or_404(Track, id_track=track_id)
    proyectos = Proyecto.objects.filter(id_track=track)
    solicitudes_proyectos = ProyectoRequest.objects.filter(
        alumno=request.user, estado='pendiente', proyecto__in=proyectos
    ).values_list('proyecto_id', flat=True)

    context = {
        'track_id': track_id,
        'track': track,
        'proyectos': proyectos,
        'proyectos_solicitados': set(solicitudes_proyectos),
    }
    return render(request, 'tracks/proyectos/lista_proyectos.html', context)

# Solicitar ingreso a proyecto


@login_required
@rol_requerido('alumno')
def solicitar_ingreso_proyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    if ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists():
        messages.warning(request, "Ya enviaste una solicitud a este proyecto.")
    else:
        ProyectoRequest.objects.create(proyecto=proyecto, alumno=request.user)
        messages.success(request, "Solicitud enviada correctamente.")
    return redirect(request.META.get('HTTP_REFERER'))

# Gestionar solicitudes de proyectos


@login_required
@rol_requerido('alumno')
def gestionar_solicitudes_proyecto(request):
    perfil = request.user.perfil_alumno
    proyectos = Proyecto.objects.filter(jefe_proyecto=perfil)
    solicitudes = ProyectoRequest.objects.filter(
        proyecto__in=proyectos, estado='pendiente')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('accion')
        solicitud = get_object_or_404(
            ProyectoRequest, id_solicitud=solicitud_id, proyecto__in=proyectos)

        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'

        solicitud.save()
        messages.success(request, f'Solicitud {accion}ada correctamente.')
        return redirect('gestionar-solicitudes-proyecto')

    return render(request, 'mis-proyectos/solicitudes/solicitudes_proyecto.html', {'solicitudes': solicitudes})

# Vista dinámica del detalle del track


@login_required
@rol_requerido('alumno')
def detalle_track_view(request, slug):
    track = get_object_or_404(Track, nom_track__iexact=slug.replace('-', ' '))
    solicitud_pendiente = TrackRequest.objects.filter(
        track=track, alumno=request.user, estado='pendiente').exists()

    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion')
    proyectos = Proyecto.objects.filter(id_track=track)
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track)
    reuniones = ReunionTrack.objects.filter(track=track)

    context = {
        'track': track,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': not request.user.id_track,
        'posts': posts,
        'proyectos': proyectos,
        'alumnos': alumnos,
        'reuniones': reuniones,
    }
    return render(request, 'tracks/home_track/detalle_track.html', context)


@login_required
@rol_requerido('alumno')
def reuniones_alumno_view(request):
    track = request.user.id_track  # Asumimos que el alumno tiene asignado un track
    reuniones = ReunionTrack.objects.filter(track=track).order_by('-fecha')

    context = {
        'reuniones': reuniones,
    }
    return render(request, 'reuniones/reuniones_alumno.html', context)


@login_required
@rol_requerido('alumno')
def eventos_track_view(request):
    eventos = Evento.objects.all().order_by(
        '-fecha_evento')  # ✅ Sin filtro por track

    context = {
        'eventos': eventos,
    }
    return render(request, 'eventos/lista_eventos.html', context)


@login_required
@rol_requerido('alumno')
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.filter(
        alumno=request.user).order_by('-fecha_creacion')
    return render(request, 'solicitudes/listar.html', {'solicitudes': solicitudes})


@login_required
@rol_requerido('alumno')
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.alumno = request.user
            solicitud.save()
            return redirect('listar-solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear.html', {'form': form})


@login_required
@rol_requerido('alumno')
def modificar_solicitud(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk, alumno=request.user)
    if solicitud.estado != 'pendiente':
        return redirect('listar-solicitudes')

    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('listar-solicitudes')
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'solicitudes/modificar.html', {'form': form})
