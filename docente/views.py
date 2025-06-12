from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido
from administrador.models import Track, TrackRequest, ReunionTrack
from django.shortcuts import get_object_or_404
from .models import PerfilDocente, Evento, DocentePost
from .forms import EventoForm, PerfilDocenteForm
from django.http import HttpResponseForbidden
from django import forms
from alumno.models import Perfil_alumno
from django.contrib import messages
from alumno.models import Proyecto
from .forms import ProyectoDocenteForm


# Create your views here.


@login_required
@rol_requerido('docente')
def home_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    return render(request, 'home-docente.html', {'track': track})


@login_required
@rol_requerido('docente')
def ver_perfil_docente(request):
    perfil, created = PerfilDocente.objects.get_or_create(docente=request.user)
    return render(request, 'perfil/ver_perfil_docente.html', {'perfil': perfil})


@login_required
@rol_requerido('docente')
def editar_perfil_docente(request):
    perfil = get_object_or_404(PerfilDocente, docente=request.user)
    if request.method == 'POST':
        form = PerfilDocenteForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('ver-perfil-doc')
    else:
        form = PerfilDocenteForm(instance=perfil)
    return render(request, 'perfil/editar_perfil_docente.html', {'form': form})


# @login_required
# @rol_requerido('docente')
# def solicitudes_pendientes_view(request):
#     if request.user.rol != 'docente':
#         return render(request, 'error.html', {'mensaje': 'No autorizado'})

#     track = Track.objects.filter(id_usuario=request.user).first()

#     if not track:
#         return render(request, 'error.html', {'mensaje': 'No tienes un track asignado'})

#     solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente')

#     return render(request, 'solicitudes/solicitudes-alumnos.html', {
#         'track': track,
#         'solicitudes': solicitudes
#     })

@login_required
@rol_requerido('docente')
def solicitudes_pendientes_view(request):
    if request.user.rol != 'docente':
        messages.error(
            request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home-docente')

    track = Track.objects.filter(id_usuario=request.user).first()

    if not track:
        messages.warning(
            request, 'No tienes un track asignado. Contacta con el administrador.')
        return redirect('home-docente')  # o a otra vista que tenga sentido

    solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente')
    return render(request, 'solicitudes/solicitudes-alumnos.html', {
        'track': track,
        'solicitudes': solicitudes
    })


@login_required
@rol_requerido('docente')
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(TrackRequest, id_solicitud=solicitud_id)

    solicitud.estado = 'aprobada'
    solicitud.save()

    usuario_alumno = solicitud.alumno
    usuario_alumno.id_track = solicitud.track
    usuario_alumno.save()

    return redirect('solicitudes_pendientes')


@login_required
@rol_requerido('docente')
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(TrackRequest, id_solicitud=solicitud_id)

    solicitud.estado = 'rechazado'
    solicitud.save()
    return redirect('solicitudes_pendientes')


@login_required
@rol_requerido('docente')
def listar_eventos(request):
    eventos = Evento.objects.filter(docente=request.user)
    return render(request, 'evento/listar_eventos.html', {'eventos': eventos})


@login_required
@rol_requerido('docente')
def añadir_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.docente = request.user
            evento.save()
            return redirect('listar-eventos')
    else:
        form = EventoForm()
    return render(request, 'evento/añadir_evento.html', {'form': form})


@login_required
@rol_requerido('docente')
def modificar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, docente=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar-eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'evento/modificar_evento.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, docente=request.user)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar-eventos')
    return render(request, 'evento/eliminar_evento.html', {'evento': evento})


class DocentePostForm(forms.ModelForm):
    class Meta:
        model = DocentePost
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuerpo o descripción'}),
        }


class ReunionTrackForm(forms.ModelForm):
    class Meta:
        model = ReunionTrack
        fields = ['fecha', 'hora', 'modalidad',
                  'link_virtual', 'ubicacion', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'link_virtual': forms.URLInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


@login_required
@rol_requerido('docente')
def mi_track_view(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    posts = DocentePost.objects.filter(track=track).order_by(
        '-fecha_creacion') if track else []
    post_form = DocentePostForm()
    return render(request, 'track/mi_track.html', {'track': track, 'posts': posts, 'post_form': post_form})


@login_required
@rol_requerido('docente')
def crear_post_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    if request.method == 'POST' and track:
        form = DocentePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.docente = request.user
            post.track = track
            post.save()
    return redirect('mi-track')


@login_required
@rol_requerido('docente')
def eliminar_post_docente(request, post_id):
    post = DocentePost.objects.get(id=post_id)
    if post.docente != request.user:
        return HttpResponseForbidden()
    post.delete()
    return redirect('mi-track')


@login_required
@rol_requerido('docente')
def modificar_post_docente(request, post_id):
    post = DocentePost.objects.get(id=post_id)
    if post.docente != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DocentePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('mi-track')
    else:
        form = DocentePostForm(instance=post)
    track = post.track
    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion')
    return render(request, 'track/mi_track.html', {'track': track, 'posts': posts, 'post_form': form, 'edit_post_id': post.id})


@login_required
@rol_requerido('docente')
def listado_alumnos_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    alumnos = Perfil_alumno.objects.filter(
        alumno__id_track=track) if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'alumnos_list': alumnos,
        'central_content': 'alumnos',
    })


@login_required
@rol_requerido('docente')
def eliminar_alumno_track(request, alumno_id):
    track = Track.objects.filter(id_usuario=request.user).first()
    alumno = Perfil_alumno.objects.get(pk=alumno_id)
    if request.method == 'POST':
        user = alumno.alumno
        user.id_track = None
        user.save()
        return redirect('listado-alumnos-track')
    return render(request, 'track/confirmar_eliminar_alumno.html', {'alumno': alumno})


@login_required
@rol_requerido('docente')
def listado_solicitudes_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    solicitudes = TrackRequest.objects.filter(
        track=track, estado='pendiente') if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'solicitudes_list': solicitudes,
        'central_content': 'solicitudes',
    })


@login_required
@rol_requerido('docente')
def listado_eventos_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    eventos = Evento.objects.filter(docente=request.user) if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'eventos_list': eventos,
        'central_content': 'eventos',
    })


""" @login_required
@rol_requerido('docente')
def crear_reunion_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    if request.method == 'POST' and track:
        form = ReunionTrackForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.id_docente = request.user
            reunion.track = track
            reunion.save()
            return redirect('mi-track')
    else:
        form = ReunionTrackForm()
    return render(request, 'track/crear_reunion.html', {'form': form, 'track': track})


@login_required
@rol_requerido('docente')
def detalle_reunion_track(request, reunion_id):
    reunion = ReunionTrack.objects.get(pk=reunion_id)
    track = reunion.track
    return render(request, 'track/detalle_reunion.html', {'reunion': reunion, 'track': track}) """


@login_required
@rol_requerido('docente')
def listar_reuniones_track(request):
    reuniones = ReunionTrack.objects.filter(id_docente=request.user)
    return render(request, 'reuniones/listar_reuniones.html', {'reuniones': reuniones})


@login_required
@rol_requerido('docente')
def crear_reunion_track(request):
    if request.method == 'POST':
        form = ReunionTrackForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.id_docente = request.user

            # Obtener el track asociado al docente
            track = Track.objects.filter(id_usuario=request.user).first()
            if not track:
                messages.error(request, "No tienes un track asignado.")
                return redirect('mi-track')

            reunion.track = track
            reunion.save()
            messages.success(request, "Reunión creada correctamente.")
            return redirect('listar-reuniones-track')
    else:
        form = ReunionTrackForm()

    return render(request, 'reuniones/crear_reunion.html', {'form': form})


@login_required
@rol_requerido('docente')
def editar_reunion_track(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk, id_docente=request.user)
    if request.method == 'POST':
        form = ReunionTrackForm(request.POST, instance=reunion)
        if form.is_valid():
            form.save()
            return redirect('listar-reuniones-track')
    else:
        form = ReunionTrackForm(instance=reunion)
    return render(request, 'reuniones/editar_reunion.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_reunion_track(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk, id_docente=request.user)
    if request.method == 'POST':
        reunion.delete()
        return redirect('listar-reuniones-track')
    return render(request, 'reuniones/eliminar_reunion.html', {'reunion': reunion})


@login_required
@rol_requerido('docente')
def detalle_reunion_modal(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk)
    return render(request, 'reuniones/detalle_reunion.html', {'reunion': reunion})


# proyecto


@login_required
@rol_requerido('docente')
def listar_proyectos_docente(request):
    proyectos = Proyecto.objects.all()  # O filtrar por track si corresponde
    return render(request, 'proyectos/listar_proyectos_docente.html', {'proyectos': proyectos})


@login_required
@rol_requerido('docente')
def crear_proyecto_docente(request):
    if request.method == 'POST':
        form = ProyectoDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar-proyectos-docente')
    else:
        form = ProyectoDocenteForm()
    return render(request, 'proyectos/crear_proyecto_docente.html', {'form': form})


@login_required
@rol_requerido('docente')
def modificar_proyecto_docente(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoDocenteForm(
            request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('listar-proyectos-docente')
    else:
        form = ProyectoDocenteForm(instance=proyecto)
    return render(request, 'proyectos/modificar_proyecto_docente.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_proyecto_docente(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar-proyectos-docente')
    return render(request, 'proyectos/eliminar_proyecto_docente.html', {'proyecto': proyecto})
