from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido
from administrador.models import Track, TrackRequest, ReunionTrack
from django.shortcuts import get_object_or_404
from .models import PerfilDocente, Evento, DocentePost
from .forms import PerfilFormDocente, EventoForm
from django.http import HttpResponseForbidden
from django import forms
from alumno.models import Perfil_alumno

# Create your views here.

@login_required
@rol_requerido('docente')
def home_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    return render(request, 'home-docente.html', {'track': track})

@login_required
@rol_requerido('docente')
def editar_perfil_docente(request):

    perfil = PerfilDocente.objects.get(docente=request.user)


    if request.method == 'POST':
        form = PerfilFormDocente(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home-docente') 
    else:
        form = PerfilFormDocente(instance=perfil)

    context = {
        'form': form,
    }
    return render(request, 'perfil-docente/editar_perfil.html', context)

@login_required
@rol_requerido('docente')
def solicitudes_pendientes_view(request):
    if request.user.rol != 'docente':
        return render(request, 'error.html', {'mensaje': 'No autorizado'})

    track = Track.objects.filter(id_usuario=request.user).first()

    if not track:
        return render(request, 'error.html', {'mensaje': 'No tienes un track asignado'})

    solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente')

    return render(request, 'track/solicitudes/solicitudes-alumnos.html', {
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
        fields = ['fecha', 'hora', 'modalidad', 'link_virtual', 'ubicacion', 'descripcion']
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
    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion') if track else []
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
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track) if track else []
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
    solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente') if track else []
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

@login_required
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
    return render(request, 'track/detalle_reunion.html', {'reunion': reunion, 'track': track})